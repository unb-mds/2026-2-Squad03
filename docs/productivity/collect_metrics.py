import os
import json
import datetime
from collections import defaultdict, Counter
from github import Github

def main():
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    if not token or not repo_name:
        raise ValueError("GITHUB_TOKEN and GITHUB_REPOSITORY must be set")

    g = Github(token)
    repo = g.get_repo(repo_name)

    # Collect all issues
    issues = list(repo.get_issues(state='all'))

    # Collect all commits
    commits = list(repo.get_commits())

    # Collect users
    users = {}
    for issue in issues:
        user = issue.user
        if user:
            users[user.login] = {'name': user.name or user.login, 'login': user.login}
    for commit in commits:
        author = commit.author
        if author:
            users[author.login] = {'name': author.name or author.login, 'login': author.login}

    # Issues per week
    issues_per_week = defaultdict(lambda: {'opened': 0, 'closed': 0})
    all_weeks = set()
    for issue in issues:
        created_week = issue.created_at.isocalendar()
        week_str = f"{created_week[0]}-W{created_week[1]:02d}"
        issues_per_week[week_str]['opened'] += 1
        all_weeks.add(week_str)
        if issue.closed_at:
            closed_week = issue.closed_at.isocalendar()
            week_str_closed = f"{closed_week[0]}-W{closed_week[1]:02d}"
            issues_per_week[week_str_closed]['closed'] += 1
            all_weeks.add(week_str_closed)

    issues_per_week_list = [{'week': w, 'opened': issues_per_week[w]['opened'], 'closed': issues_per_week[w]['closed']} for w in sorted(all_weeks)]

    # Commit message histogram
    ranges = ['0-20', '21-50', '51-100', '101-200', '200+']
    hist = Counter()
    for commit in commits:
        msg = commit.commit.message
        length = len(msg)
        if length <= 20:
            hist['0-20'] += 1
        elif length <= 50:
            hist['21-50'] += 1
        elif length <= 100:
            hist['51-100'] += 1
        elif length <= 200:
            hist['101-200'] += 1
        else:
            hist['200+'] += 1
    commit_message_histogram = [{'range': r, 'count': hist[r]} for r in ranges]

    # Co-authors per week
    coauthors_per_week = defaultdict(int)
    for commit in commits:
        dt = commit.commit.author.date
        week = dt.isocalendar()
        week_str = f"{week[0]}-W{week[1]:02d}"
        message = commit.commit.message
        coauthors = sum(1 for line in message.split('\n') if line.strip().startswith('Co-authored-by:'))
        coauthors_per_week[week_str] += coauthors
        all_weeks.add(week_str)

    coauthors_per_week_list = [{'week': w, 'count': coauthors_per_week[w]} for w in sorted(all_weeks)]

    # Commit heatmap
    commit_heatmap = defaultdict(int)
    for commit in commits:
        dt = commit.commit.author.date
        day = dt.weekday()  # 0=Mon
        hour = dt.hour
        commit_heatmap[(day, hour)] += 1
    commit_heatmap_list = [{'day': d, 'hour': h, 'count': c} for (d, h), c in commit_heatmap.items()]

    # Top committers
    committers = defaultdict(int)
    for commit in commits:
        author = commit.author
        username = author.login if author else 'ghost'
        committers[username] += 1
    top_committers = [{'username': u, 'name': users.get(u, {}).get('name', u), 'commits': c} for u, c in sorted(committers.items(), key=lambda x: x[1], reverse=True)]

    # Top PR authors
    pr_authors = defaultdict(int)
    for issue in issues:
        if issue.pull_request:
            username = issue.user.login if issue.user else 'ghost'
            pr_authors[username] += 1
    top_pr_authors = [{'username': u, 'name': users.get(u, {}).get('name', u), 'prs_opened': c} for u, c in sorted(pr_authors.items(), key=lambda x: x[1], reverse=True)]

    # Top issue contributors
    opened = defaultdict(int)
    closed = defaultdict(int)
    for issue in issues:
        username = issue.user.login if issue.user else 'ghost'
        opened[username] += 1
        if issue.closed_at:
            closed[username] += 1
    total = {k: opened[k] + closed[k] for k in set(opened) | set(closed)}
    top_issue_contributors = [{'username': u, 'name': users.get(u, {}).get('name', u), 'opened': opened[u], 'closed': closed[u], 'total': total[u]} for u in sorted(total, key=total.get, reverse=True)]

    # Generated at
    generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Data
    data = {
        "generated_at": generated_at,
        "repository": repo_name,
        "issues_per_week": issues_per_week_list,
        "commit_message_histogram": commit_message_histogram,
        "coauthors_per_week": coauthors_per_week_list,
        "commit_heatmap": commit_heatmap_list,
        "top_committers": top_committers,
        "top_pr_authors": top_pr_authors,
        "top_issue_contributors": top_issue_contributors
    }

    with open('metrics.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    main()