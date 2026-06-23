from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.models import NoticiaModel as Noticia
from backend.app.models import RegiaoModel as Regiao
from backend.app.schemas.noticia import NoticiaCreate, NoticiaResponse
import json
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON # Esta é a função principal
from sqlalchemy import func

router = APIRouter(
    prefix="/mapa",
    tags=["Mapas e Regiões"]
)

# 📱 Endpoint para o Front-end listar os locais que possuem alertas/notícias
@router.get("/")
def ler_noticias_mapa(db: Session = Depends(get_db)):
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
