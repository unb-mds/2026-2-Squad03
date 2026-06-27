"""
Modelos ORM (Object-Relational Mapping) do VeritasIA.

Este módulo define as entidades do banco de dados utilizando a base declarativa 
do SQLAlchemy. Ele engloba as tabelas de Usuários, Regiões Monitoradas (com 
suporte a dados geoespaciais via PostGIS) e Notícias, estabelecendo também os 
relacionamentos entre elas.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base
from geoalchemy2 import Geometry

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class UsuarioModel(Base):
    """
    Modelo de representação da tabela de usuários.

    Armazena as credenciais e dados básicos das pessoas que têm acesso ao sistema.

    Attributes:
        id (Integer): Chave primária gerada automaticamente.
        nome (String): Nome completo do usuário.
        email (String): Endereço de e-mail do usuário (único e indexado para buscas rápidas).
        senha (String): Hash da senha do usuário para autenticação segura.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class RegiaoModel(Base):
    """
    Modelo de representação das regiões geográficas monitoradas pelo sistema.

    Armazena o nome e a localização em coordenadas geográficas da região, 
    permitindo o vínculo direto com as notícias coletadas nessa área.

    Attributes:
        id (Integer): Chave primária gerada automaticamente.
        nome (String): Nome descritivo da região monitorada.
        geom (Geometry): Coluna espacial que armazena a coordenada (Ponto) da região usando 
            a projeção WGS 84 (SRID 4326). Requer a extensão PostGIS ativa no banco.
        noticias (relationship): Relacionamento (1:N) indicando as notícias associadas 
            a esta região. Se a região for excluída, todas as suas notícias também serão 
            removidas em cascata (`delete-orphan`).
    """
    __tablename__ = "regioes_monitoradas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)

    geom = Column(Geometry('POINT', srid=4326), nullable=False) # Armazena a geometria como WKT (Well-Known Text)

    # Relacionamento bidirecional: permite acessar as notícias desta região facilmente
    noticias = relationship("NoticiaModel", back_populates="regiao", cascade="all, delete-orphan")

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class NoticiaModel(Base):
    """
    Modelo de representação das notícias processadas.

    Armazena todas as informações extraídas, sumarizadas e classificadas sobre uma notícia 
    coletada na web, além de manter um vínculo de chave estrangeira com a região 
    geográfica relacionada.

    Attributes:
        id (Integer): Chave primária gerada automaticamente.
        titulo (String): Título ou manchete original da notícia.
        fonte_url (String): Link original da notícia (único e indexado).
        conteudo (String): Texto integral ou parcial extraído (mapeado para o tipo TEXT).
        resumo_raw (String): Resumo bruto gerado por IA (mapeado para o tipo TEXT).
        resumo_blur (String): Resumo com aplicação de filtros/anonimização, se aplicável (mapeado para TEXT).
        data_publicacao (DateTime): Data original em que a notícia foi publicada.
        Portal (String): Nome do veículo de imprensa ou site de origem.
        data_no_banco (DateTime): Carimbo de tempo do momento exato em que o registro foi salvo no banco.
        regiao_id (Integer): Chave estrangeira que aponta para `id` em `regioes_monitoradas`. 
            Regra `CASCADE` garante exclusão segura.
        regiao (relationship): Objeto referencial da região vinculada, permitindo acesso inverso.
    """
    __tablename__ = "noticias"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(300), nullable=False)
    fonte_url = Column(String(500), unique=True, index=True, nullable=False)
    conteudo = Column(String, nullable=True) # Mapeia para o tipo TEXT do Postgres
    resumo_raw = Column(String, nullable=True) # Mapeia para o tipo TEXT do Postgres
    resumo_blur = Column(String, nullable=True) # Mapeia para o tipo TEXT do Postgres
    data_publicacao = Column(DateTime, default=datetime.utcnow)
    Portal = Column(String, nullable=False)
    data_no_banco = Column(DateTime, default=datetime.utcnow)

    # A nossa famosa Chave Estrangeira (Foreign Key)
    regiao_id = Column(Integer, ForeignKey("regioes_monitoradas.id", ondelete="CASCADE"), nullable=False)
    
    # Aponta de volta para o modelo da Região
    regiao = relationship("RegiaoModel", back_populates="noticias")
    
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+