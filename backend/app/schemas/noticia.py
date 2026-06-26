from pydantic import BaseModel
from datetime import datetime

# Um schema simples para a região que vai dentro da notícia
class RegiaoParcialResponse(BaseModel):
    id: int
    nome: str
    sigla: str | None = None

    class Config:
        from_attributes = True # Antigo orm_mode = True no Pydantic v2

# O seu schema de resposta atualizado
class NoticiaResponse(BaseModel):
    id: int
    titulo: str
    resumo_blur: str 
    resumo_raw: str 
    Portal: str
    fonte_url: str
    data_publicacao: datetime
    regiao_id: int
    regiao: RegiaoParcialResponse | None = None # <--- ESSA LINHA ADICIONA A REGIÃO NO JSON

    class Config:
        from_attributes = True