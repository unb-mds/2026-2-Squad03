from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)


class RegiaoModel(Base):
    __tablename__ = "regioes_monitoradas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Relacionamento bidirecional: permite aceder às notícias desta região facilmente
    noticias = relationship("NoticiaModel", back_populates="regiao", cascade="all, delete-orphan")


class NoticiaModel(Base):
    __tablename__ = "noticias"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(300), nullable=False)
    url = Column(String(500), unique=True, index=True, nullable=False)
    resumo = Column(String, nullable=True) # Mapeia para o tipo TEXT do Postgres
    data_publicacao = Column(DateTime, default=datetime.utcnow)
    sentimento = Column(String(50), nullable=True)

    # A nossa famosa Chave Estrangeira (Foreign Key)
    regiao_id = Column(Integer, ForeignKey("regioes_monitoradas.id", ondelete="CASCADE"), nullable=False)
    
    # Aponta de volta para o modelo da Região
    regiao = relationship("RegiaoModel", back_populates="noticias")