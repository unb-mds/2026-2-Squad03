"""
test_dashboard_routes.py
=========================

Cobre o endpoint `GET /dashboard/`.

A função `dashboard()` no código de produção executa, NESTA ORDEM:
    1. get_ultimas_noticias()   -> 1x .all()
    2. get_estatisticas()       -> 3x .count()
    3. portais()                -> 5x .count()  (g1, cnn, r7, metropoles, total)
    4. get_noticias_por_dia_e_data() -> 1x .all()
    5. get_noticias_por_regiao()     -> 1x .all()
    6. get_noticias_por_estado()     -> 1x .all()

Os testes abaixo configuram `query_mock.all.side_effect` e
`query_mock.count.side_effect` respeitando essa ordem.

AJUSTE DE IMPORT: confirmado via main.py — o módulo real é
backend.app.adapters.api_adapter.dashboard_routes
"""

from datetime import datetime, timedelta

import pytest

from backend.app.database import get_db
from backend.app.adapters.api_adapter import dashboard_routes
from backend.tests.factories import fake_noticia, fake_regiao


@pytest.fixture
def dashboard_client(client_factory):
    return client_factory(dashboard_routes.router, get_db)


def _configure_happy_path(query_mock):
    """Configura um cenário "feliz" com dados plausíveis para todas as 6 sub-rotinas."""
    agora = datetime.now()

    noticia = fake_noticia(id=10, titulo="Tiroteio no centro", Portal="G1", data_publicacao=agora)
    regiao = fake_regiao(nome="São Paulo, SP")

    # 1) get_ultimas_noticias -> .all()
    ultimas_noticias_result = [(noticia, regiao)]

    # 4) get_noticias_por_dia_e_data -> .all() (tuplas: data_dia, total)
    dia_e_data_result = [
        (agora.date() - timedelta(days=1), 5),
        (agora.date(), 8),
    ]

    # 5) get_noticias_por_regiao -> .all() (linhas com Regiao.nome)
    regiao_rows_1 = [("São Paulo, SP",), ("Recife, PE",), (None,)]

    # 6) get_noticias_por_estado -> .all()
    regiao_rows_2 = [("São Paulo, SP",), ("Recife, PE",)]

    query_mock.all.side_effect = [
        ultimas_noticias_result,
        dia_e_data_result,
        regiao_rows_1,
        regiao_rows_2,
    ]

    # get_estatisticas: total_hoje, total_semana_atual, total_semana_anterior
    # portais: g1, cnn, r7, metropoles, total
    query_mock.count.side_effect = [
        50,  # total_hoje
        20,  # total_semana_atual
        10,  # total_semana_anterior
        12,  # g1
        3,   # cnn
        2,   # r7
        1,   # metropoles
        50,  # total (para percentuais)
    ]


def test_dashboard_retorna_200_e_estrutura_completa(dashboard_client, query_mock):
    _configure_happy_path(query_mock)

    response = dashboard_client.get("/dashboard/")

    assert response.status_code == 200
    payload = response.json()

    for chave in (
        "latest_news",
        "estatisticas",
        "top_portais",
        "noticias_semana",
        "top_regioes",
        "noticias_por_estado",
    ):
        assert chave in payload


def test_dashboard_calcula_crescimento_percentual_corretamente(dashboard_client, query_mock):
    _configure_happy_path(query_mock)

    response = dashboard_client.get("/dashboard/")
    estatisticas = response.json()["estatisticas"][0]

    # (20 - 10) / 10 * 100 = 100.0
    assert estatisticas["crescimento_percentual"] == 100.0
    assert estatisticas["total_semana"] == 20
    assert estatisticas["media_diaria"] == round(20 / 7, 2)


def test_dashboard_crescimento_quando_nao_havia_semana_anterior(dashboard_client, query_mock):
    """Quando total_semana_anterior == 0 e há notícias na semana atual, crescimento deve ser 100%."""
    query_mock.all.side_effect = [[], [], [], []]
    query_mock.count.side_effect = [
        5,  # total_hoje
        5,  # total_semana_atual
        0,  # total_semana_anterior
        0, 0, 0, 0,  # portais
        5,  # total
    ]

    response = dashboard_client.get("/dashboard/")
    estatisticas = response.json()["estatisticas"][0]

    assert estatisticas["crescimento_percentual"] == 100.0


def test_dashboard_banco_vazio_nao_gera_divisao_por_zero(dashboard_client, query_mock):
    """Banco totalmente vazio: percentuais de portais e regiões devem ser 0, sem exceção."""
    query_mock.all.side_effect = [[], [], [], []]
    query_mock.count.side_effect = [0, 0, 0, 0, 0, 0, 0, 0]

    response = dashboard_client.get("/dashboard/")

    assert response.status_code == 200
    payload = response.json()

    for portal in payload["top_portais"]:
        assert portal["value"] == 0
        assert portal["percent"] == 0

    for regiao in payload["top_regioes"]:
        assert regiao["value"] == 0


def test_dashboard_agrupa_regioes_por_macro_regiao_via_regex(dashboard_client, query_mock):
    agora = datetime.now()
    query_mock.all.side_effect = [
        [],  # ultimas noticias
        [],  # noticias por dia
        [("Recife, PE",), ("Porto Alegre, RS",), ("Manaus, AM",), ("Texto sem UF",)],  # top_regioes
        [("Recife, PE",), ("Porto Alegre, RS",), ("Manaus, AM",)],  # por estado
    ]
    query_mock.count.side_effect = [0, 0, 0, 0, 0, 0, 0, 0]

    response = dashboard_client.get("/dashboard/")
    payload = response.json()

    regioes = {item["name"]: item["value"] for item in payload["top_regioes"]}
    assert regioes["Nordeste"] == 1  # PE
    assert regioes["Sul"] == 1       # RS
    assert regioes["Norte"] == 1     # AM

    assert payload["noticias_por_estado"] == {"PE": 1, "RS": 1, "AM": 1}


def test_dashboard_ultimas_noticias_inclui_nome_da_regiao(dashboard_client, query_mock):
    agora = datetime.now()
    noticia = fake_noticia(id=99, titulo="Furto em loja", Portal="CNN", data_publicacao=agora)
    regiao = fake_regiao(nome="Brasília, DF")

    query_mock.all.side_effect = [
        [(noticia, regiao)],
        [],
        [],
        [],
    ]
    query_mock.count.side_effect = [0, 0, 0, 0, 0, 0, 0, 0]

    response = dashboard_client.get("/dashboard/")
    latest = response.json()["latest_news"]

    assert len(latest) == 1
    assert latest[0]["titulo"] == "Furto em loja"
    assert latest[0]["regiao"] == "Brasília, DF"
