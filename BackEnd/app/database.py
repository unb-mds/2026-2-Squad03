import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Recupera a URL do banco. Se não encontrar no .env, usa uma local padrão
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/veritas_db"
)

# A Engine é o motor que gerencia a comunicação com o Postgres (seja local ou no Supabase)
engine = create_engine(DATABASE_URL)

# O SessionLocal é quem abre as portas para fazermos consultas e salvamentos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A Base que os nossos Models (models.py) usam para criar as tabelas
Base = declarative_base()

# Função que o FastAPI usa para abrir e fechar a conexão nas rotas automaticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()