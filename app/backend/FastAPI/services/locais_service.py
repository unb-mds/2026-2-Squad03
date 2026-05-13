from sqlalchemy.orm import Session
from app.backend.FastAPI.models.local import Local
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

def criar_local(db: Session, nome: str, lat: float, lon: float):
    ponto = from_shape(Point(lon, lat), srid=4326)
    local = Local(nome=nome, geom=ponto)
    db.add(local)
    db.commit()
    db.refresh(local)
    return local

def listar_locais(db: Session):
    return db.query(Local).all()

def buscar_local(db: Session, id: int):
    return db.query(Local).filter(Local.id == id).first()

def atualizar_local(db: Session, id: int, nome: str, lat: float, lon: float):
    local = db.query(Local).filter(Local.id == id).first()
    if not local:
        return None

    local.nome = nome
    local.geom = from_shape(Point(lon, lat), srid=4326)

    db.commit()
    db.refresh(local)
    return local

def deletar_local(db: Session, id: int):
    local = db.query(Local).filter(Local.id == id).first()
    if not local:
        return None

    db.delete(local)
    db.commit()
    return True