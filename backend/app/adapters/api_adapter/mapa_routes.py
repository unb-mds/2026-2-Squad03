"""
Rotas para visualização de dados geográficos no mapa.

Este módulo gerencia os endpoints responsáveis por fornecer dados espaciais 
para o frontend. Ele cruza as informações de notícias com as geometrias 
das regiões monitoradas e formata a saída no padrão internacional GeoJSON, 
permitindo fácil integração com bibliotecas de mapas web (como Leaflet ou Mapbox).

Informações Úteis:
    - Padrão GeoJSON: A rota não retorna uma lista simples, mas sim um objeto 
      estruturado do tipo `FeatureCollection`, exigido nativamente por renderizadores de mapas.
    - Otimização Espacial: O processamento das coordenadas é delegado ao banco 
      de dados via PostGIS (função `ST_AsGeoJSON`), aliviando a CPU do backend.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json

from backend.app.database import get_db
from backend.app.models import NoticiaModel as Noticia
from backend.app.models import RegiaoModel as Regiao
from backend.app.schemas.noticia import NoticiaResponse

# Importações para manipulação de dados espaciais no banco
from geoalchemy2.functions import ST_AsGeoJSON # Esta é a função principal
from sqlalchemy import func

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# Roteador do FastAPI dedicado aos endpoints de mapas e geolocalização.
# O prefixo "/mapa" define a raiz das requisições geoespaciais.
router = APIRouter(
    prefix="/mapa",
    tags=["Mapas e Regiões"]
)

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# 📱 Endpoint para o Front-end listar os locais que possuem alertas/notícias
@router.get("/")
def ler_noticias_mapa(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Recupera as notícias e suas respectivas localizações estruturadas em GeoJSON.

    Realiza uma consulta (JOIN) unindo as tabelas de Notícias e Regiões. Utiliza 
    a função `ST_AsGeoJSON` do PostGIS no nível do banco para converter dados 
    binários (WKB/WKT) em strings JSON geográficas. Notícias vinculadas a regiões 
    sem uma geometria válida associada são descartadas em tempo de execução 
    para não quebrar a renderização no frontend.

    Variáveis de Escopo:
        resultados (list[tuple]): Retorno cru do banco contendo tuplas de objetos 
            `Noticia` e strings geoespaciais.
        features (list[dict]): Lista de dicionários representando os nós do mapa (pinos).
        noticia (Noticia): Instância do modelo SQLAlchemy iterada no loop.
        geom (str | None): O JSON geográfico retornado pelo banco de dados.

    Args:
        db (Session, optional): Sessão ativa de conexão com o banco de dados.

    Returns:
        dict: Um payload contendo `{"type": "FeatureCollection", "features": [...]}`. 
            Cada `Feature` injeta a geometria e anexa propriedades essenciais da 
            notícia (id, título, resumo bruto e portal veículo) para exibição de popups.
    """
    # Buscamos a Notícia e a Geometria (Região) juntas em uma única query
    resultados = db.query(Noticia, Regiao.geom).join(Regiao).all()
    
    features = []
    for noticia, geom in resultados:
        # Monta a estrutura rigorosa de uma Feature GeoJSON
        features.append({
            "type": "Feature",
            # ST_AsGeoJSON retorna uma string no banco, o json.loads a converte para dicionário Python
            "geometry": json.loads(db.scalar(ST_AsGeoJSON(geom))) if geom is not None else None,
            "properties": {
                "id": noticia.id,            # Incluímos o ID para hiperlinks e roteamento
                "data": noticia.data_publicacao,
                "titulo": noticia.titulo,
                "resumo": noticia.resumo_raw, # Incluímos o resumo gerado pela IA
                "veiculo": noticia.Portal,
            }
        })
        
        # Filtro de Integridade: Impede o envio de nós fantasmas (sem coordenadas) para o mapa
        if features[-1]["geometry"] is None:
            features.pop()  # Remove a feature recém adicionada se a geometria for nula
            print(f"⚠️ Geometria nula ignorada para a notícia: {noticia.titulo}")
            
    
    return {"type": "FeatureCollection", "features": features}

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+