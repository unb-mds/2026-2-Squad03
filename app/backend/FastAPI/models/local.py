from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from app.backend.FastAPI.models.base import Base

class Local(Base):
    __tablename__ = "locais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    geom = Column(Geometry("POINT", srid=4326))