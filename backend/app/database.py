"""
Módulo de configuração e conexão com o banco de dados.

Este módulo gerencia a inicialização da conexão com o banco de dados usando SQLAlchemy.
Ele carrega as variáveis de ambiente, configura a engine de conexão, define a base
declarativa para os modelos e fornece um gerador para injeção de sessões do
banco de dados nas rotas do FastAPI.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# Carrega o arquivo .env
load_dotenv(dotenv_path='.env', encoding='utf-8')

# Lê a URL do ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# Verifica se a URL foi carregada (ajuda a debugar)
if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não foi encontrada. Verifique seu arquivo .env!")

engine = create_engine(DATABASE_URL)
"""Engine principal do SQLAlchemy conectada ao banco de dados."""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Fábrica de sessões configurada para interagir com o banco de dados de forma isolada."""

Base = declarative_base()
"""Classe base declarativa do SQLAlchemy para a definição dos modelos ORM."""

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def get_db():
    """
    Fornece uma sessão de banco de dados isolada por requisição.

    Esta função atua como um gerador (generator) e foi desenhada para ser usada 
    como uma dependência (Dependency Injection) no FastAPI. Ela garante que a
    sessão seja aberta no momento em que a requisição chega e fechada com 
    segurança após o término do processamento, evitando vazamento de conexões.

    Yields:
        Session: Uma instância de sessão do SQLAlchemy conectada ao banco.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+