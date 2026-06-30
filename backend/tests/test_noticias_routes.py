"""
test_noticias_routes.py
=========================

Cobre `GET /noticias/` e `GET /noticias/{id}`.

Agora que o schema real (backend/app/schemas/noticia.py) e os modelos
(backend/app/models.py) estão disponíveis, os testes usam `TestClient`
de ponta a ponta, validando inclusive a serialização Pydantic
(from_attributes=True), o aninhamento de `regiao` e o erro 404.

AJUSTE DE IMPORT: confirmado via main.py — o módulo real é
backend.app.adapters.api_adapter.noticias_routes
"""

from datetime import datetime

import pytest

from backend.app.database import get_db
from backend.app.adapters.api_adapter import noticias_routes
from backend.tests.factories import fake_noticia, fake_regiao


@pytest.fixture
def noticias_client(client_factory):
    return client_factory(noticias_routes.router, get_db)


def test_listar_noticias_retorna_200_com_regiao_aninhada(noticias_client, query_mock):
    regiao = fake_regiao(id=3, nome="Salvador, BA")
    noticia = fake_noticia(
        id=1,
        titulo="Notícia A",
        fonte_url="https://exemplo.com/a",
        data_publicacao=datetime(2026, 5, 1, 8, 0, 0),
        regiao_id=3,
        regiao=regiao,
    )
    query_mock.all.return_value = [noticia]

    response = noticias_client.get("/noticias/")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["titulo"] == "Notícia A"
    assert payload[0]["regiao"]["nome"] == "Salvador, BA"
    assert payload[0]["regiao"]["sigla"] is None  # RegiaoModel não tem esse campo


def test_listar_noticias_aplica_offset_via_query_param(noticias_client, query_mock):
    query_mock.all.return_value = []

    response = noticias_client.get("/noticias/?skip=25")

    assert response.status_code == 200
    assert query_mock.calls["offset"] == [((25,), {})]


def test_listar_noticias_lista_vazia_retorna_array_vazio(noticias_client, query_mock):
    query_mock.all.return_value = []

    response = noticias_client.get("/noticias/")

    assert response.status_code == 200
    assert response.json() == []


def test_listar_noticias_falha_serializacao_quando_campo_obrigatorio_falta(noticias_client, query_mock):
    """
    NoticiaResponse exige resumo_blur, resumo_raw, Portal, fonte_url,
    data_publicacao e regiao_id como NAO opcionais. Se o ORM devolver um
    objeto sem algum desses campos (ex.: coluna nula indevidamente), o
    Pydantic recusa a serializacao.

    NOTA: por padrao, o `starlette.testclient.TestClient` PROPAGA exceções
    levantadas dentro da aplicação (em vez de convertê-las numa resposta
    HTTP 500, como um servidor ASGI real faria via Uvicorn). Por isso o
    teste verifica a exceção diretamente com `pytest.raises`, em vez de
    checar `response.status_code == 500`. Esse comportamento evidencia a
    importância de um `NOT NULL` no banco e/ou de o `joinedload` carregar
    a região corretamente antes de a resposta ser montada.
    """
    from fastapi.exceptions import ResponseValidationError

    noticia_incompleta = fake_noticia(resumo_raw=None)  # campo obrigatorio ausente
    query_mock.all.return_value = [noticia_incompleta]

    with pytest.raises(ResponseValidationError):
        noticias_client.get("/noticias/")


def test_ler_noticia_retorna_200_quando_encontrada(noticias_client, query_mock):
    noticia = fake_noticia(id=7, titulo="Noticia encontrada")
    query_mock.first.return_value = noticia

    response = noticias_client.get("/noticias/7")

    assert response.status_code == 200
    assert response.json()["id"] == 7
    assert response.json()["titulo"] == "Noticia encontrada"


def test_ler_noticia_retorna_404_quando_nao_encontrada(noticias_client, query_mock):
    query_mock.first.return_value = None

    response = noticias_client.get("/noticias/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Notícia não encontrada"


def test_ler_noticia_com_id_invalido_retorna_422(noticias_client):
    """O path param `id: int` deve rejeitar valores nao numericos antes de tocar o banco."""
    response = noticias_client.get("/noticias/abc")

    assert response.status_code == 422