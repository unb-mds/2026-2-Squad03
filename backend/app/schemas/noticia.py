from pydantic import BaseModel, ConfigDict, HttpUrl
from datetime import datetime
from typing import Optional

# Dados que o Scraper PRECISA enviar ao cadastrar uma notícia
class NoticiaCreate(BaseModel):
    titulo: str
    conteudo: str
    resumo_raw: Optional[str] = None
    resumo_blur: Optional[str] = None
    fonte_url: str
    data_publicacao: Optional[datetime] = None
    localizacao_texto: Optional[str] = None  # Ex: "Brasília, DF"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# Dados que a API vai RETORNAR (inclui o ID criado pelo banco)
class NoticiaResponse(BaseModel):
    id: int
    titulo: str
    fonte_url: str
    conteudo: Optional[str] = None
    resumo_raw: Optional[str] = None
    resumo_blur: Optional[str] = None
    data_publicacao: Optional[datetime] = None
    regiao_id: int

    # O from_attributes = True é a chave para o SQLAlchemy funcionar no Pydantic v2
    model_config = ConfigDict(from_attributes=True)