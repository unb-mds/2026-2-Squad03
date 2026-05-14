# app/routers/locais.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from FastAPI.schemas.local import LocalCreate, LocalUpdate
from FastAPI.services import locais_service

router = APIRouter(prefix="/locais", tags=["Locais"])

# Injeta a sessão de conexão ao banco de dados isolada por requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=201)
def criar(local: LocalCreate, db: Session = Depends(get_db)):
    return locais_service.criar_local(
        db,
        local.nome,
        local.latitude,
        local.longitude
    )

@router.get("/")
def listar(db: Session = Depends(get_db)):
    return locais_service.listar_locais(db)

@router.get("/{id}")
def buscar(id: int, db: Session = Depends(get_db)):
    local = locais_service.buscar_local(db, id)
    if not local:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return local

@router.put("/{id}")
def atualizar(id: int, local: LocalUpdate, db: Session = Depends(get_db)):
    atualizado = locais_service.atualizar_local(
        db,
        id,
        local.nome,
        local.latitude,
        local.longitude
    )
    if not atualizado:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return atualizado

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    removido = locais_service.deletar_local(db, id)
    if not removido:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return {"message": "Local removido com sucesso"}