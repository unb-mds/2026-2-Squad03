#!/usr/bin/env python3
"""Coleta métricas públicas do GitHub e gera docs/productivity/metrics.json.

Idempotência: sempre reescreve o arquivo completo.

Entradas via variáveis de ambiente:
- GITHUB_TOKEN (obrigatório)
- GITHUB_REPOSITORY (owner/repo, obrigatório)
- GITHUB_API_URL (opcional)

"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Tuple

from github import Auth, Github
from github.Repository import Repository


COAUTHORED_BY_RE = re.compile(
    r"^Co-authored-by:\s*(.+?)\s*<([^>]+)>\s*$",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass
class PersonAgg:
    username: str
    name: str
    avatar_url: str
    commits: int = 0
    prs_opened: int = 0
    issues_opened: int = 0
    issues_closed: int = 0

    def to_top_committers(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "name": self.name,
            "commits": self.commits,
            "avatar_url": self.avatar_url,
        }

    def to_top_pr_authors(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "name": self.name,
            "prs_opened": self.prs_opened,
            "avatar_url": self.avatar_url,
        }

    def to_top_issue_contributors(self) -> Dict[str, Any]:
        total = self.issues_opened + self.issues_closed
        return {
            "username": self.username,
            "name": self.name,
            "opened": self.issues_opened,
            "closed": self.issues_closed,
            "total": total,
            "avatar_url": self.avatar_url,
        }


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_week_key(dt: datetime) -> str:
    iso_year, iso_week, _ = dt.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def normalize_username(user: Any) -> str:
    return getattr(user, "login", None) or str(user)


def parse_coauthors(commit_message: str) -> List[Tuple[str, str]]:
    if not commit_message:
        return []

    out: List[Tuple[str, str]] = []
    for m in COAUTHORED_BY_RE.finditer(commit_message):
        name = (m.group(1) or "").strip()
        email = (m.group(2) or "").strip().lower()
        if not name or not email or "@" not in email:
            continue
        out.append((name, email))
    return out


def classify_commit_message_histogram(message: str) -> str:
    n = len(message or "")
    if n <= 20:
        return "0-20"
    if n <= 50:
        return "21-50"
    if n <= 100:
        return "51-100"
    if n <= 200:
        return "101-200"
    return "200+"


def ensure_days_hours_heatmap(dataset: Dict[Tuple[int, int], int]) -> List[Dict[str, int]]:
    # Mantém apenas bins com dados; a UI pode inferir ausência como zero.
    return [
        {"day": day, "hour": hour, "count": count}
        for (day, hour), count in sorted(dataset.items(), key=lambda x: (x[0][0], x[0][1]))
        if count
    ]


def build_issue_week_aggregates(repo: Repository) -> Tuple[Dict[str, int], Dict[str, int]]:
    opened_by_week: Dict[str, int] = defaultdict(int)
    closed_by_week: Dict[str, int] = defaultdict(int)

    since = datetime.now(timezone.utc) - timedelta(weeks=104)

    # repo.get_issues também pode retornar PRs; filtramos.
    for state, target in [("open", opened_by_week), ("closed", closed_by_week)]:
        for issue in repo.get_issues(state=state, since=since, direction="desc"):
            if issue.pull_request is not None:
                continue
            if state == "open":
                week = parse_week_key(issue.created_at)
                target[week] += 1
            else:
                closed_at = getattr(issue, "closed_at", None)
                if closed_at is None:
                    continue
                week = parse_week_key(closed_at)
                target[week] += 1

    return opened_by_week, closed_by_week


def build_commit_aggregates(
    repo: Repository,
) -> Tuple[
    Dict[str, int],
    Dict[str, int],
    Dict[Tuple[int, int], int],
    Dict[str, PersonAgg],
]:
    commit_hist: Dict[str, int] = defaultdict(int)
    coauthors_by_week: Dict[str, int] = defaultdict(int)
    heatmap_bins: Dict[Tuple[int, int], int] = defaultdict(int)
    persons: Dict[str, PersonAgg] = {}

    since = datetime.now(timezone.utc) - timedelta(weeks=104)

    for commit in repo.get_commits(since=since):
        author = getattr(commit, "author", None)
        author_login = getattr(author, "login", None) if author is not None else None
        if not author_login:
            author_login = "unknown"

        if author_login not in persons:
            author_name = getattr(author, "name", None) if author is not None else None
            avatar_url = getattr(author, "avatar_url", None) if author is not None else None
            persons[author_login] = PersonAgg(
                username=author_login,
                name=author_name or author_login,
                avatar_url=avatar_url or "",
            )

        persons[author_login].commits += 1

        commit_obj = getattr(commit, "commit", None)
        message = getattr(commit_obj, "message", "") if commit_obj is not None else ""
        bucket = classify_commit_message_histogram(message)
        commit_hist[bucket] += 1

        # heatmap by commit timestamp
        timestamp = None
        if commit_obj is not None:
            dt = getattr(getattr(commit_obj, "author", None), "date", None)
            if dt is None:
                dt = getattr(getattr(commit_obj, "committer", None), "date", None)
            timestamp = dt

        if timestamp is None:
            continue

        dt_utc = timestamp.astimezone(timezone.utc)
        week = parse_week_key(dt_utc)
        heatmap_bins[(dt_utc.weekday(), dt_utc.hour)] += 1

        coauthors = parse_coauthors(message)
        if coauthors:
            coauthors_by_week[week] += len(coauthors)

    return commit_hist, coauthors_by_week, heatmap_bins, persons


def build_pr_opened_aggregates(repo: Repository) -> Dict[str, PersonAgg]:
    persons: Dict[str, PersonAgg] = {}
    since = datetime.now(timezone.utc) - timedelta(weeks=104)

    # Não enviar base=None (PyGithub quebra). O filtro por branch não é exigido na spec.
    for pr in repo.get_pulls(state="open", sort="created", direction="desc"):
        if pr.created_at < since:
            continue

        user = pr.user
        username = normalize_username(user)
        if username not in persons:
            persons[username] = PersonAgg(
                username=username,
                name=getattr(user, "name", None) or username,
                avatar_url=getattr(user, "avatar_url", None) or "",
            )
        persons[username].prs_opened += 1

    return persons


def build_issue_contributors(repo: Repository, persons: Dict[str, PersonAgg]) -> Dict[str, PersonAgg]:
    since = datetime.now(timezone.utc) - timedelta(weeks=104)

    for state in ["open", "closed"]:
        for issue in repo.get_issues(state=state, since=since, direction="desc"):
            if issue.pull_request is not None:
                continue

            user = issue.user
            username = normalize_username(user)
            if username not in persons:
                persons[username] = PersonAgg(
                    username=username,
                    name=getattr(user, "name", None) or username,
                    avatar_url=getattr(user, "avatar_url", None) or "",
                )

            if state == "open":
                persons[username].issues_opened += 1
            else:
                persons[username].issues_closed += 1

    return persons


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    repo_full = os.environ.get("GITHUB_REPOSITORY")

    if not token:
        print("Erro: GITHUB_TOKEN não definido.", file=sys.stderr)
        return 2
    if not repo_full:
        print("Erro: GITHUB_REPOSITORY não definido.", file=sys.stderr)
        return 2

    # Failsafe: nunca gravar dados mockados/placeholder.
    # Se algo falhar durante a coleta, aborta com erro para que o workflow não commite JSON inválido.


    api_url = os.environ.get("GITHUB_API_URL")

    auth = Auth.Token(token)
    github = Github(auth=auth, base_url=api_url) if api_url else Github(auth=auth)
    repo = github.get_repo(repo_full)

    issues_open, issues_closed = build_issue_week_aggregates(repo)
    commit_hist, coauthors_by_week, heatmap_bins, committers = build_commit_aggregates(repo)
    pr_openers = build_pr_opened_aggregates(repo)

    # merge PRs into same persons (for rankings)
    for username, pdata in pr_openers.items():
        if username not in committers:
            committers[username] = pdata
        else:
            committers[username].prs_opened = pdata.prs_opened

    committers = build_issue_contributors(repo, committers)

    weeks = sorted(set(list(issues_open.keys()) + list(issues_closed.keys())))
    issues_per_week = [
        {"week": w, "opened": issues_open.get(w, 0), "closed": issues_closed.get(w, 0)}
        for w in weeks
    ]

    histogram_order = ["0-20", "21-50", "51-100", "101-200", "200+"]
    commit_message_histogram = [
        {"range": r, "count": int(commit_hist.get(r, 0))} for r in histogram_order
    ]

    coauthors_per_week = [
        {"week": w, "count": int(coauthors_by_week.get(w, 0))}
        for w in sorted(coauthors_by_week.keys())
    ]

    commit_heatmap = ensure_days_hours_heatmap(heatmap_bins)

    # Top 10 (ou menos, se não houver tantos)
    top_committers = sorted(committers.values(), key=lambda p: p.commits, reverse=True)[:10]
    top_pr_authors = sorted(committers.values(), key=lambda p: p.prs_opened, reverse=True)[:10]
    top_issue_contributors = sorted(
        committers.values(),
        key=lambda p: (p.issues_opened + p.issues_closed),
        reverse=True,
    )[:10]

    out = {
        "generated_at": utc_now_iso(),
        "repository": repo_full,
        "issues_per_week": issues_per_week,
        "commit_message_histogram": commit_message_histogram,
        "coauthors_per_week": coauthors_per_week,
        "commit_heatmap": commit_heatmap,
        "top_committers": [p.to_top_committers() for p in top_committers],
        "top_pr_authors": [p.to_top_pr_authors() for p in top_pr_authors],
        "top_issue_contributors": [p.to_top_issue_contributors() for p in top_issue_contributors],
    }

    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(base_dir, exist_ok=True)
    out_path = os.path.join(base_dir, "metrics.json")

    # Failsafe anti-mock (ajustado): sempre escrever metrics.json.
    # Em caso de falha parcial/0 dados, o dashboard exibirá séries vazias/0 em vez de ficar preso em mock.


    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Gerado: {out_path}")
    try:
        sz = os.path.getsize(out_path)
        print(f"Tamanho do arquivo: {sz} bytes")
    except Exception as e:
        print(f"Falha ao obter tamanho do arquivo: {e}", file=sys.stderr)

    # Debug rápido do conteúdo (evita mock/arquivo vazio sem perceber)
    try:
        with open(out_path, "r", encoding="utf-8") as f:
            preview = f.read(300)
        preview_clean = preview.replace("\n", " ").replace("\r", " ")
        print(f"Preview: {preview_clean}")
    except Exception as e:
        print(f"Falha ao ler preview: {e}", file=sys.stderr)

    return 0





if __name__ == "__main__":
    raise SystemExit(main())

