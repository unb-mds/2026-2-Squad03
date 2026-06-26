"""
Schemas de validação e serialização de dados (Pydantic).

Este módulo define os modelos Pydantic utilizados para validar os dados de 
entrada (requests) vindos dos scrapers e serializar os dados de saída (responses) 
enviados pela API. Eles garantem que a estrutura dos dados esteja correta antes 
de qualquer interação com o banco de dados.
"""

from pydantic import BaseModel, ConfigDict, HttpUrl
from datetime import datetime
from typing import Optional, Any

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class NoticiaCreate(BaseModel):
    """
    Schema de validação para a criação de uma nova notícia.

    Define os dados estritos que o Scraper (ou outro cliente) PRECISA enviar 
    no corpo da requisição (payload) ao cadastrar uma notícia no sistema.
    (Atualmente o sistema de backend NÃO recebe informações do scraper, 
    o scraper confere e faz upload para o banco de dados diretamente)

    Attributes:
        titulo (str): Título ou manchete da notícia.
        conteudo (str): Texto integral ou extraído da notícia.
        resumo_raw (Optional[str]): Resumo original gerado automaticamente (opcional).
        resumo_blur (Optional[str]): Resumo com filtro/anonimização aplicado (opcional).
        fonte_url (str): Link de origem da notícia.
        data_publicacao (Optional[datetime]): Data e hora original da publicação (opcional).
        localizacao_texto (Optional[str]): Nome da localização identificada no texto, ex: "Brasília, DF" (opcional).
        latitude (Optional[float]): Coordenada de latitude extraída ou inferida (opcional).
        longitude (Optional[float]): Coordenada de longitude extraída ou inferida (opcional).
    """
    titulo: str
    conteudo: str
    resumo_raw: Optional[str] = None
    resumo_blur: Optional[str] = None
    fonte_url: str
    data_publicacao: Optional[datetime] = None
    localizacao_texto: Optional[str] = None  # Ex: "Brasília, DF"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class NoticiaResponse(BaseModel):
    """
    Schema de serialização para a resposta de dados de uma notícia.

    Define a estrutura dos dados que a API vai RETORNAR ao cliente após uma 
    consulta. Inclui campos gerados internamente pelo banco de dados, como IDs.

    Attributes:
        id (int): Identificador único da notícia no banco de dados.
        titulo (str): Título da notícia.
        fonte_url (str): Link de origem da notícia.
        conteudo (Optional[str]): Texto integral da notícia.
        resumo_raw (Optional[str]): Resumo original gerado pela IA.
        resumo_blur (Optional[str]): Resumo com filtros aplicados.
        data_publicacao (Optional[datetime]): Data de publicação da notícia.
        regiao_id (int): Identificador da região geográfica vinculada a esta notícia.
    """
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
    
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class RegiaoResponse(BaseModel):
    """
    Schema de serialização para a resposta de dados de uma região monitorada.

    Estrutura os dados de retorno quando a API precisa listar ou detalhar as 
    regiões geográficas cadastradas.

    Attributes:
        id (int): Identificador único da região no banco de dados.
        nome (str): Nome descritivo da região.
    """
    id: int
    nome: str
    
    class Config:
        from_attributes = True