# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Altere os valores abaixo de acordo com as credenciais locais do seu PostgreSQL
DATABASE_URL = "postgresql://postgres:senha@localhost:5432/gis"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)