from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

# Dados que o Scraper PRECISA enviar ao cadastrar uma notícia
class NoticiaCreate(BaseModel):
    titulo: str
    conteudo: str
    fonte_url: str
    data_publicacao: Optional[datetime] = None
    localizacao_texto: Optional[str] = None  # Ex: "Brasília, DF"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# Dados que a API vai RETORNAR (inclui o ID criado pelo banco)
class NoticiaResponse(BaseModel):
    id: int
    titulo: str
    conteudo: str
    fonte_url: str
    data_publicacao: Optional[datetime]
    localizacao_texto: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    data_coleta: datetime

    class Config:
        from_attributes = True  # Permite que o Pydantic leia modelos do SQLAlchemy