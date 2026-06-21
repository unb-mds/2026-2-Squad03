from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.models import NoticiaModel as Noticia
from backend.app.schemas.noticia import NoticiaCreate, NoticiaResponse

router = APIRouter(
    prefix="/locais",
    tags=["Locais e Notícias"]
)

# 🚀 Endpoint para o Scraper injetar notícias com coordenadas geográficas
@router.post("/noticias", response_model=NoticiaResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_noticia_local(noticia: NoticiaCreate, db: Session = Depends(get_db)):
    # Evita duplicados pela URL da fonte
    noticia_existente = db.query(Noticia).filter(Noticia.fonte_url == noticia.fonte_url).first()
    if noticia_existente:
        raise HTTPException(
            status_code=400, 
            detail="Esta notícia já foi catalogada no sistema."
        )
    
    nova_noticia = Noticia(
        titulo=noticia.titulo,
        conteudo=noticia.conteudo,
        fonte_url=noticia.fonte_url,
        data_publicacao=noticia.data_publicacao,
        localizacao_texto=noticia.localizacao_texto,
        latitude=noticia.latitude,
        longitude=noticia.longitude
    )
    
    db.add(nova_noticia)
    db.commit()
    db.refresh(nova_noticia)
    return nova_noticia

# 📱 Endpoint para o Front-end listar os locais que possuem alertas/notícias
@router.get("/noticias", response_model=List[NoticiaResponse])
def listar_noticias_locais(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Noticia).offset(skip).limit(limit).all()