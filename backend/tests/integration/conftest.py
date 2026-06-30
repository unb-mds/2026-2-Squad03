"""
Fixtures para os testes de INTEGRACAO (banco real) com Schema Isolado.

Este módulo configura um ambiente seguro para rodar testes diretamente no 
projeto Supabase de produção, utilizando um schema isolado (por padrão, "test").

## Correção Definitiva de Isolamento (schema_translate_map)
Em vez de depender de `search_path` (um parâmetro de sessão fragilizado sob 
connection pooling como o PgBouncer), este módulo utiliza o `schema_translate_map` 
do SQLAlchemy. 
Isso reescreve a instrução SQL no momento da compilação. Qualquer referência a 
uma tabela com `schema=None` é qualificada como `test.nome_da_tabela`. Isso 
torna a operação totalmente explícita e independente do backend físico que o 
PgBouncer alocar.

## Setup Necessário
1. Rode `setup_test_schema.sql` no SQL Editor do Supabase (cria o schema "test").
2. Exporte a variável `TEST_DATABASE_URL` (pode ser a mesma de produção).

COMO RODAR:
`pytest -m integration backend/tests/integration/ -v`
"""

import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.app.database import Base
from backend.app import models  # noqa: F401  (garante que os modelos sejam registrados em Base.metadata)

# Configurações de ambiente
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
TEST_SCHEMA = os.getenv("TEST_SCHEMA", "test")

# Tabelas esperadas no schema de teste para a verificação ativa.
_TABELAS_ESPERADAS = {"noticias", "regioes_monitoradas", "usuarios"}

requires_test_db = pytest.mark.skipif(
    not TEST_DATABASE_URL,
    reason="TEST_DATABASE_URL nao definida — testes de integracao pulados. "
    "Configure TEST_DATABASE_URL para rodar esta suite.",
)


def _garantir_schema_existe(engine_bootstrap):
    """Cria o schema de teste se ele ainda não existir (idempotente)."""
    if TEST_SCHEMA == "public":
        raise RuntimeError(
            "TEST_SCHEMA está configurado como 'public' — isso anularia todo "
            "o isolamento dos testes de integração contra dados reais. "
            "Use um nome diferente (padrão: 'test')."
        )

    with engine_bootstrap.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA};"))
        conn.commit()

        existe = conn.execute(
            text("SELECT 1 FROM information_schema.schemata WHERE schema_name = :nome"),
            {"nome": TEST_SCHEMA},
        ).scalar()

        if not existe:
            raise RuntimeError(
                f"Falha ao criar/confirmar o schema de teste '{TEST_SCHEMA}'. "
                "Verifique se o usuário do banco tem permissão CREATE SCHEMA."
            )


def _confirmar_tabelas_no_schema_de_teste(engine_bootstrap):
    """
    Verificação ATIVA: confere no information_schema.tables se as tabelas existem.
    """
    with engine_bootstrap.connect() as conn:
        tabelas_no_schema = {
            row[0]
            for row in conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = :schema"),
                {"schema": TEST_SCHEMA},
            ).all()
        }

    faltando = _TABELAS_ESPERADAS - tabelas_no_schema
    if faltando:
        raise RuntimeError(
            f"FALHA DE ISOLAMENTO: as tabelas {faltando} não existem dentro do "
            f"schema '{TEST_SCHEMA}' depois do create_all. Abortando operação."
        )


@pytest.fixture(scope="session")
def integration_engine():
    """Gerencia a criação e destruição do pool de conexões principal de testes."""
    if not TEST_DATABASE_URL:
        pytest.skip("TEST_DATABASE_URL nao definida")

    bootstrap_engine = create_engine(TEST_DATABASE_URL)
    try:
        _garantir_schema_existe(bootstrap_engine)

        with bootstrap_engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
            conn.commit()
    finally:
        bootstrap_engine.dispose()

    # Aplicação do redirecionamento transparente de schema.
    engine = create_engine(TEST_DATABASE_URL).execution_options(
        schema_translate_map={None: TEST_SCHEMA}
    )

    Base.metadata.create_all(bind=engine)
    _confirmar_tabelas_no_schema_de_teste(create_engine(TEST_DATABASE_URL))

    yield engine

    engine.dispose()


@pytest.fixture
def db_session(integration_engine):
    """
    Sessão isolada por teste.
    Abre transação, faz bind da Session e dá ROLLBACK ao final.
    """
    connection = integration_engine.connect()
    trans = connection.begin()

    SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionTesting()

    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()


@pytest.fixture(scope="session", autouse=True)
def _opcional_dropar_schema_no_final(integration_engine):
    """Remove o schema 'test' completamente se TEST_SCHEMA_DROP_AFTER=1 for exportado."""
    yield

    if os.getenv("TEST_SCHEMA_DROP_AFTER") == "1" and TEST_DATABASE_URL:
        bootstrap_engine = create_engine(TEST_DATABASE_URL)
        try:
            with bootstrap_engine.connect() as conn:
                conn.execute(text(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE;"))
                conn.commit()
        finally:
            bootstrap_engine.dispose()


@pytest.fixture
def seed_regiao(db_session):
    """Factory fixture para inserir uma RegiaoModel de teste."""
    from geoalchemy2.elements import WKTElement
    from backend.app.models import RegiaoModel

    def _seed(nome="Cidade Teste, DF", lon=-47.93, lat=-15.78):
        regiao = RegiaoModel(
            nome=nome,
            geom=WKTElement(f"POINT({lon} {lat})", srid=4326),
        )
        db_session.add(regiao)
        db_session.flush()
        return regiao

    return _seed


@pytest.fixture
def seed_noticia(db_session, seed_regiao):
    """Factory fixture para inserir uma NoticiaModel de teste."""
    from datetime import datetime
    from backend.app.models import NoticiaModel

    def _seed(regiao=None, **overrides):
        if regiao is None:
            regiao = seed_regiao()

        defaults = dict(
            titulo="Noticia de teste",
            fonte_url=f"https://exemplo.com/teste-{os.urandom(4).hex()}",
            conteudo="Conteudo de teste.",
            resumo_raw="Resumo raw de teste.",
            resumo_blur="Resumo blur de teste.",
            data_publicacao=datetime(2026, 1, 1, 12, 0, 0),
            Portal="G1",
            regiao_id=regiao.id,
        )
        defaults.update(overrides)

        noticia = NoticiaModel(**defaults)
        db_session.add(noticia)
        db_session.flush()
        return noticia

    return _seed