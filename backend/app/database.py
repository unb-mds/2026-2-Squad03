"""
Configuração da camada de persistência e conexão com o banco de dados.

Este módulo centraliza a lógica de conexão com o PostgreSQL/Supabase utilizando 
o SQLAlchemy como ORM. Ele é responsável pelo ciclo de vida das conexões, 
garantindo que cada requisição HTTP receba uma sessão isolada e que os 
recursos sejam liberados após o uso.

Informações Úteis:
    - Injeção de Dependência: O método `get_db` é o padrão de mercado para 
      FastAPI, garantindo que você nunca precise abrir ou fechar sessões 
      manualmente dentro das rotas.
    - Segurança: A URL de conexão é carregada via `.env`, garantindo que 
      credenciais sensíveis não sejam versionadas no repositório.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# Carregamento das variáveis de ambiente a partir do arquivo .env.
load_dotenv(dotenv_path='.env', encoding='utf-8')

# URL de conexão ao banco de dados (ex: postgresql://user:password@host:port/db)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não foi encontrada. Verifique seu arquivo .env!")

# Engine principal do SQLAlchemy: o objeto que gerencia o pool de conexões.
engine = create_engine(DATABASE_URL)

# Fábrica de sessões: instância que produz novas sessões (Session) para interagir com o banco.
# autocommit=False e autoflush=False garantem controle manual e seguro sobre as transações.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos ORM (tabelas).
Base = declarative_base()

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def get_db():
    """
    Dependency Injection Generator: Fornece uma sessão de banco isolada por requisição.

    Esta função é o padrão recomendado pelo FastAPI para gerenciar o escopo de 
    sessões do SQLAlchemy. Ela garante que uma conexão seja aberta ao iniciar a 
    rota (`yield db`) e, independentemente de sucesso ou erro (graças ao `finally`), 
    a conexão é estritamente fechada (`db.close()`), prevenindo o esgotamento do 
    pool de conexões no Supabase.

    Yields:
        Session: Uma instância de sessão configurada para a transação corrente.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+