from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.models import NoticiaModel as Noticia
from backend.app.schemas.noticia import NoticiaCreate, NoticiaResponse

router = APIRouter(
    prefix="/noticias",
    tags=["Locais e Notícias"]
)

# 📱 Endpoint para o Front-end listar os locais que possuem alertas/notícias
@router.get("/", response_model=List[NoticiaResponse])
def listar_noticias_locais(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    noticias = db.query(Noticia).offset(skip).limit(limit).all()
    print(noticias)
    return noticias