#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, schema
from sqlalchemy.orm import sessionmaker
from backend.app.main import app
from backend.app.database import Base, get_db

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# Configuração de um banco SQLite em memória para testes rápidos
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine) # Cria as tabelas do models.py [7]
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]
    
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+
    
from backend.app.models import NoticiaModel

def test_listar_noticias_vazio(client):
    """Verifica se a lista de notícias começa vazia."""
    response = client.get("/noticias/")
    assert response.status_code == 200
    assert response.json() == []

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def test_ler_noticia_por_id_sucesso(client, db):
    """Cria uma notícia no banco e tenta recuperá-la por ID."""
    nova_noticia = NoticiaModel(
        titulo="Caso Exemplo", 
        conteudo="Conteúdo da notícia", 
        fonte_url="http://g1.com",
        regiao_id=1
    )
    db.add(nova_noticia)
    db.commit()

    response = client.get(f"/noticias/{nova_noticia.id}")
    assert response.status_code == 200
    assert response.json()["titulo"] == "Caso Exemplo"

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def test_ler_noticia_nao_encontrada(client):
    """Verifica o erro 404 para IDs inexistentes [8]."""
    response = client.get("/noticias/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Notícia não encontrada"

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def test_login_sucesso(client):
    """Testa a rota de login com dados válidos."""
    payload = {"email": "usuario@teste.com", "senha": "123"}
    # Nota: A lógica interna do login precisa ser implementada no backend [10]
    response = client.post("/auth/login", json=payload)
    
    # Se o login for simulado como sucesso:
    assert response.status_code == 200
    assert "token" in response.json()
    
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+