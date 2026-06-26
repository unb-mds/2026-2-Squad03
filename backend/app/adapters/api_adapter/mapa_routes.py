"""
Rotas para visualização de dados geográficos no mapa.

Este módulo gerencia os endpoints responsáveis por fornecer dados espaciais 
para o frontend. Ele cruza as informações de notícias com as geometrias 
das regiões monitoradas e formata a saída no padrão internacional GeoJSON, 
permitindo fácil integração com bibliotecas de mapas.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from backend.app.database import get_db
from backend.app.models import NoticiaModel as Noticia
from backend.app.models import RegiaoModel as Regiao
from backend.app.schemas.noticia import NoticiaResponse

# Importações para manipulação de dados espaciais no banco
from geoalchemy2.functions import ST_AsGeoJSON # Esta é a função principal
from sqlalchemy import func

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

router = APIRouter(
    prefix="/mapa",
    tags=["Mapas e Regiões"]
)
"""Roteador do FastAPI dedicado aos endpoints de mapas e geolocalização."""

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# 📱 Endpoint para o Front-end listar os locais que possuem alertas/notícias
@router.get("/")
def ler_noticias_mapa(db: Session = Depends(get_db)):
    """
    Recupera todas as notícias e suas respectivas localizações em formato GeoJSON.

    Realiza uma consulta no banco de dados unindo as tabelas de Notícias e Regiões.
    Utiliza a função `ST_AsGeoJSON` do PostGIS para converter as coordenadas (geometria)
    em um formato JSON padrão de mapas. Notícias cujas regiões não possuem geometria
    válida são automaticamente filtradas e logadas no terminal.

    Args:
        db (Session, optional): Sessão do banco de dados injetada automaticamente 
            pelo FastAPI.

    Returns:
        dict: Um dicionário estruturado como uma `FeatureCollection` do padrão GeoJSON,
            contendo uma lista de `features`. Cada feature possui sua geometria (ponto) 
            e as propriedades da notícia (id, título, resumo e veículo).
    """
    # Buscamos a Notícia e a Geometria (Região)
    resultados = db.query(Noticia, Regiao.geom).join(Regiao).all()
    
    features = []
    for noticia, geom in resultados:
        features.append({
            "type": "Feature",
            "geometry": json.loads(db.scalar(ST_AsGeoJSON(geom))) if geom is not None else None,
            "properties": {
                "id": noticia.id,            # Incluímos o ID
                "titulo": noticia.titulo,
                "resumo": noticia.resumo_raw, # Incluímos o resumo
                "veiculo": noticia.Portal,
            }
        
        })
        if features[-1]["geometry"] is None:
            features.pop()  # Remove a feature se a geometria for nula
            print(f"Geometria nula para a notícia: {noticia.titulo}")
            
    
    return {"type": "FeatureCollection", "features": features}

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+