"""
test_mapa_routes.py
=====================

Cobre o endpoint `GET /mapa/`.

A rota faz: db.query(Noticia, Regiao.geom).join(Regiao).all() e, para CADA
linha com geom não-nulo, chama db.scalar(ST_AsGeoJSON(geom)).

Por isso configuramos:
    - query_mock.all.return_value -> lista de tuplas (noticia, geom_raw)
    - db.scalar.side_effect -> uma string JSON por chamada (na MESMA ordem
      das linhas cujo geom não é None)

AJUSTE DE IMPORT: confirmado via main.py — o módulo real é
backend.app.adapters.api_adapter.mapa_routes
"""

import json

import pytest

from backend.app.database import get_db
from backend.app.adapters.api_adapter import mapa_routes
from backend.tests.factories import fake_noticia


@pytest.fixture
def mapa_client(client_factory):
    return client_factory(mapa_routes.router, get_db)


def test_mapa_retorna_feature_collection_valida(mapa_client, mock_db, query_mock):
    noticia = fake_noticia(id=1, titulo="Roubo de veículo", Portal="R7", resumo_raw="Resumo X")
    geom_raw = object()  # representaria a coluna geometry vinda do PostGIS

    query_mock.all.return_value = [(noticia, geom_raw)]
    mock_db.scalar.side_effect = [
        json.dumps({"type": "Point", "coordinates": [-47.9, -15.8]})
    ]

    response = mapa_client.get("/mapa/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "FeatureCollection"
    assert len(payload["features"]) == 1

    feature = payload["features"][0]
    assert feature["type"] == "Feature"
    assert feature["geometry"] == {"type": "Point", "coordinates": [-47.9, -15.8]}
    assert feature["properties"]["id"] == 1
    assert feature["properties"]["titulo"] == "Roubo de veículo"
    assert feature["properties"]["resumo"] == "Resumo X"
    assert feature["properties"]["veiculo"] == "R7"


def test_mapa_descarta_noticias_com_geometria_nula(mapa_client, mock_db, query_mock):
    noticia_com_geo = fake_noticia(id=1, titulo="Com geo")
    noticia_sem_geo = fake_noticia(id=2, titulo="Sem geo")

    query_mock.all.return_value = [
        (noticia_com_geo, object()),
        (noticia_sem_geo, None),
    ]
    # scalar só é chamado quando geom is not None -> 1 chamada apenas
    mock_db.scalar.side_effect = [
        json.dumps({"type": "Point", "coordinates": [0, 0]})
    ]

    response = mapa_client.get("/mapa/")
    payload = response.json()

    ids_presentes = [f["properties"]["id"] for f in payload["features"]]
    assert ids_presentes == [1]
    assert mock_db.scalar.call_count == 1


def test_mapa_sem_noticias_retorna_features_vazio(mapa_client, query_mock):
    query_mock.all.return_value = []

    response = mapa_client.get("/mapa/")
    payload = response.json()

    assert payload == {"type": "FeatureCollection", "features": []}
