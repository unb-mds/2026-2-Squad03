"""
Testes de integracao que validam as QUERIES REAIS (nao mockadas).

Estes testes validam lógicas que dependem estritamente do motor relacional, como:
- `ilike` sendo case-insensitive no Postgres
- `func.date` agrupando corretamente datas
- `ST_AsGeoJSON` do PostGIS gerando GeoJSON válido.
"""

from datetime import datetime, timedelta

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.database import get_db
from backend.app.adapters.api_adapter import dashboard_routes, mapa_routes
from backend.tests.integration.conftest import requires_test_db

# Marca TODOS os testes deste módulo como "integration"
pytestmark = pytest.mark.integration


def _client_for(router, db_session):
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = lambda: db_session
    return TestClient(app)


@requires_test_db
def test_portais_ilike_e_case_insensitive_no_postgres(db_session, seed_noticia):
    """
    Garante que o filtro `Noticia.Portal.ilike` bate com variações de caixa 
    ("G1", "g1") com igualdade exata e case-insensitive.
    """
    seed_noticia(Portal="g1")  # minúsculo de propósito
    seed_noticia(Portal="G1")
    seed_noticia(Portal="CNN")

    client = _client_for(dashboard_routes.router, db_session)
    response = client.get("/dashboard/")

    assert response.status_code == 200
    portais = {p["name"]: p["value"] for p in response.json()["top_portais"]}
    assert portais["G1"] == 2
    assert portais["CNN"] == 1


@requires_test_db
def test_agrupamento_de_noticias_por_dia_no_postgres(db_session, seed_noticia):
    """Valida que func.date() agrupa corretamente registros do mesmo dia."""
    hoje = datetime.now()
    seed_noticia(data_publicacao=hoje, fonte_url="https://exemplo.com/n1")
    seed_noticia(data_publicacao=hoje, fonte_url="https://exemplo.com/n2")
    seed_noticia(data_publicacao=hoje - timedelta(days=1), fonte_url="https://exemplo.com/n3")

    client = _client_for(dashboard_routes.router, db_session)
    response = client.get("/dashboard/")

    semana = response.json()["noticias_semana"]
    total_noticias_no_periodo = sum(d["noticias"] for d in semana)
    assert total_noticias_no_periodo == 3


@requires_test_db
def test_regiao_com_uf_e_corretamente_extraida_via_regex_no_postgres(db_session, seed_regiao, seed_noticia):
    """Verifica a extração da sigla de unidade federativa (UF) do nome completo da região."""
    regiao_sp = seed_regiao(nome="Campinas, SP", lon=-47.06, lat=-22.90)
    seed_noticia(regiao=regiao_sp, fonte_url="https://exemplo.com/sp1")

    client = _client_for(dashboard_routes.router, db_session)
    response = client.get("/dashboard/")

    estados = response.json()["noticias_por_estado"]
    assert estados.get("SP") == 1


@requires_test_db
def test_mapa_geojson_real_via_postgis(db_session, seed_regiao, seed_noticia):
    """Verifica a conversão nativa de PostGIS para GeoJSON no response."""
    regiao = seed_regiao(nome="Brasília, DF", lon=-47.93, lat=-15.78)
    seed_noticia(regiao=regiao, titulo="Ocorrência no Plano Piloto", fonte_url="https://exemplo.com/df1")

    client = _client_for(mapa_routes.router, db_session)
    response = client.get("/mapa/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "FeatureCollection"
    assert len(payload["features"]) == 1

    feature = payload["features"][0]
    assert feature["geometry"]["type"] == "Point"
    
    # PostGIS retorna [lon, lat]
    lon, lat = feature["geometry"]["coordinates"]
    assert round(lon, 2) == -47.93
    assert round(lat, 2) == -15.78