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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+