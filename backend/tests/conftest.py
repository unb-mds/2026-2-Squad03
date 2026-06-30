"""
Fixtures compartilhadas para os testes de rotas do VeritasIA.

Este módulo configura o ambiente de testes do Pytest, sobrescrevendo dependências 
reais (como a sessão do banco de dados) por instâncias controladas (Mocks).

Premissas e Ajustes:
    - Estrutura: Necessário um `__init__.py` na pasta de testes para uso de absolute imports.
    - Isolamento: `get_db` é interceptado via `app.dependency_overrides`, impedindo 
      qualquer transação real com o PostgreSQL.
    - ChainableQuery: Substituto customizado para a API fluente do SQLAlchemy (`.filter().order_by()`). 
      Evita o erro `RecursionError` que ocorre ao usar `MagicMock` que retorna a si mesmo.
"""

import sys
from types import SimpleNamespace, ModuleType
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Stub do geoalchemy2 para ambientes de teste onde a lib não está instalada.
try:
    import geoalchemy2  # noqa: F401
except ImportError:
    geoalchemy2_stub = ModuleType("geoalchemy2")
    geoalchemy2_functions_stub = ModuleType("geoalchemy2.functions")

    def _fake_st_as_geojson(geom):
        return geom

    geoalchemy2_functions_stub.ST_AsGeoJSON = _fake_st_as_geojson
    geoalchemy2_stub.functions = geoalchemy2_functions_stub
    sys.modules["geoalchemy2"] = geoalchemy2_stub
    sys.modules["geoalchemy2.functions"] = geoalchemy2_functions_stub


class ChainableQuery:
    """
    Substituto simples para a API fluente do SQLAlchemy `Query`.

    Apenas os métodos terminais (`.all`, `.count`, `.first`, `.scalar`) são 
    MagicMock. Os métodos de encadeamento (`filter`, `join`, etc.) retornam `self`, 
    eliminando problemas de autorreferência circular no traceback do pytest.
    """

    def __init__(self):
        self.all = MagicMock(name="query.all")
        self.count = MagicMock(name="query.count")
        self.first = MagicMock(name="query.first")
        self.scalar = MagicMock(name="query.scalar")
        self.calls = {}

    def _record(self, method_name, args, kwargs):
        self.calls.setdefault(method_name, []).append((args, kwargs))

    def filter(self, *args, **kwargs):
        self._record("filter", args, kwargs)
        return self

    def join(self, *args, **kwargs):
        self._record("join", args, kwargs)
        return self

    def order_by(self, *args, **kwargs):
        self._record("order_by", args, kwargs)
        return self

    def limit(self, *args, **kwargs):
        self._record("limit", args, kwargs)
        return self

    def group_by(self, *args, **kwargs):
        self._record("group_by", args, kwargs)
        return self

    def options(self, *args, **kwargs):
        self._record("options", args, kwargs)
        return self

    def offset(self, *args, **kwargs):
        self._record("offset", args, kwargs)
        return self


@pytest.fixture
def query_mock():
    """Mock único reaproveitado por toda a função de rota testada."""
    return ChainableQuery()


@pytest.fixture
def mock_db(query_mock):
    """Mock de `Session` do SQLAlchemy. `db.query(...)` sempre devolve o mesmo `query_mock`."""
    db = MagicMock(name="db_session")
    db.query = MagicMock(return_value=query_mock)
    db.scalar = MagicMock()
    return db


def make_test_app(router, get_db_dependency, mock_db):
    """Cria uma FastAPI app mínima contendo apenas o router sob teste."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db_dependency] = lambda: mock_db
    return app


@pytest.fixture
def client_factory(mock_db):
    """
    Fixture-fábrica que retorna um TestClient pronto, com o banco de dados mockado.
    """
    def _factory(router, get_db_dependency):
        app = make_test_app(router, get_db_dependency, mock_db)
        return TestClient(app)

    return _factory