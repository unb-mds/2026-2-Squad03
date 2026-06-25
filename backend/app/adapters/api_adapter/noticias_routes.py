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

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# 📱 Endpoint para o Front-end listar os locais que possuem alertas/notícias
@router.get("/", response_model=List[NoticiaResponse])
def listar_noticias_locais(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    noticias = db.query(Noticia).offset(skip).limit(limit).all()
    #print(noticias)
    return noticias

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

@router.get("/{id}", response_model=NoticiaResponse)
def ler_noticia(id: int, db: Session = Depends(get_db)):
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