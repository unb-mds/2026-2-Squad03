import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# 2. Recupera a URL do banco. Se não encontrar no .env, usa uma local padrão por segurança
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:123321123@localhost:5432/veritas_db"
)

# 3. A Engine é o motor que gerencia a comunicação e o "pool" de conexões com o Postgres
engine = create_engine(DATABASE_URL)

# 4. O SessionLocal é uma fábrica de sessões. Cada requisição na API abrirá uma sessão para conversar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. A Base declarativa que as nossas classes/models vão herdar para mapear as tabelas
Base = declarative_base()

# 6. Função utilitária (Injeção de Dependência) para abrir e fechar a conexão automaticamente nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()