"""
Rotas para listagem e consulta de notícias.

Este módulo fornece os endpoints responsáveis por expor os dados das notícias 
cadastradas no banco de dados. Permite a listagem paginada de todas as notícias 
e a busca detalhada de um artigo específico através do seu ID.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.models import NoticiaModel as Noticia
from backend.app.schemas.noticia import NoticiaCreate, NoticiaResponse

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

router = APIRouter(
    prefix="/noticias",
    tags=["Locais e Notícias"]
)
"""Roteador do FastAPI dedicado aos endpoints de notícias."""

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# 📱 Endpoint para o Front-end listar os locais que possuem alertas/notícias
@router.get("/", response_model=List[NoticiaResponse])
def listar_noticias_locais(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Lista as notícias cadastradas no banco de dados com suporte a paginação.

    Este endpoint recupera um lote de notícias, permitindo que o frontend
    controle a quantidade de dados recebidos por vez (paginação) para não 
    sobrecarregar a aplicação.

    Args:
        skip (int, optional): Número de registros para pular antes de começar 
            a retornar os resultados (Offset). Padrão é 0.
        limit (int, optional): Número máximo de registros a serem retornados 
            na requisição. Padrão é 50.
        db (Session, optional): Sessão do banco de dados injetada pelo FastAPI.

    Returns:
        List[NoticiaResponse]: Uma lista de notícias serializadas conforme 
            o schema do Pydantic.
    """
    noticias = db.query(Noticia).offset(skip).limit(limit).all()
    #print(noticias)
    return noticias

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

@router.get("/{id}", response_model=NoticiaResponse)
def ler_noticia(id: int, db: Session = Depends(get_db)):
    """
    Busca os detalhes de uma notícia específica pelo seu ID.

    Procura no banco de dados o registro exato correspondente ao ID fornecido 
    na URL. Se a notícia existir, retorna seus dados. Caso contrário, dispara 
    um erro HTTP padrão.

    Args:
        id (int): O identificador único da notícia no banco de dados.
        db (Session, optional): Sessão do banco de dados injetada pelo FastAPI.

    Raises:
        HTTPException: Erro 404 disparado caso nenhuma notícia seja encontrada 
            com o ID especificado.

    Returns:
        NoticiaResponse: Os dados da notícia serializados pelo Pydantic.
    """
    print(f"Buscando notícia com ID {id} no banco de dados...")
    noticia = db.query(Noticia).filter(Noticia.id == id).first()
    print(noticia, "Notícia encontrada no banco de dados")
    if not noticia:
        raise HTTPException(
            status_code=404, 
            detail="Notícia não encontrada"
        )
    
    return noticia

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+