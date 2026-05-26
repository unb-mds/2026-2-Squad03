from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point
from backend.app.ports.repository_port import IRegiaoRepository
from backend.app.domain.entities import RegiaoMonitorada

Base = declarative_base()

class LocalModel(Base):
    __tablename__ = "locais_monitorados"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    geom = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)

class PostGisRepositoryAdapter(IRegiaoRepository):
    def __init__(self, session: Session):
        self.session = session

    def salvar(self, regiao: RegiaoMonitorada) -> RegiaoMonitorada:
        ponto = from_shape(Point(regiao.longitude, regiao.latitude), srid=4326)
        db_model = LocalModel(nome=regiao.nome, geom=ponto)
        self.session.add(db_model)
        self.session.commit()
        self.session.refresh(db_model)
        regiao.id = db_model.id
        return regiao

    def listar_todas(self) -> list[RegiaoMonitorada]:
        registros = self.session.query(LocalModel).all()
        lista = []
        for reg in registros:
            pt = to_shape(reg.geom)
            lista.append(RegiaoMonitorada(id=reg.id, nome=reg.nome, latitude=pt.y, longitude=pt.x))
        return lista