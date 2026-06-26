"""
Rotas para alimentação de dados do Dashboard.

Este módulo fornece os endpoints necessários para calcular e retornar 
estatísticas gerais e métricas sobre as notícias processadas pelo sistema, 
alimentando os gráficos e indicadores visuais do frontend.
"""

from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy import desc # Importante para ordenar
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.models import NoticiaModel as Noticia
from backend.app.models import RegiaoModel as Regiao


#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)
"""Roteador do FastAPI dedicado aos endpoints do Dashboard."""

estatisticas = list()
"""Lista auxiliar para armazenamento temporário de estatísticas (uso interno)."""

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# 📱 Endpoint para o Front-end listar os locais que possuem alertas/notícias
@router.get("/")
def calcular_estatisticas(db: Session = Depends(get_db)):
    """
    Calcula e retorna as estatísticas principais para o Dashboard.

    Esta rota realiza cálculos comparativos entre os últimos 7 dias e a 
    semana anterior (de 14 a 7 dias atrás) para determinar o volume de 
    notícias processadas, a média diária e a taxa de crescimento percentual.
    Além disso, executa um JOIN (junção) com o modelo de Região para 
    recuperar as 3 notícias mais recentes cadastradas com seus respectivos 
    locais.

    Args:
        db (Session, optional): Sessão do banco de dados injetada automaticamente 
            pelo FastAPI.

    Returns:
        dict: Um dicionário formatado para o frontend contendo:
            - latest_news (list): As 3 últimas notícias com id, título, portal, data e região.
            - total_atual (int): Total de notícias na última semana.
            - media_diaria (float): Média de notícias por dia na última semana.
            - crescimento_percentual (float): Variação percentual de volume em relação à semana anterior.
            - total_semana (int): Cópia do total_atual para uso no gráfico semanal.
    """
    agora = datetime.now()
    uma_semana_atras = agora - timedelta(days=7)
    duas_semanas_atras = agora - timedelta(days=14)

    # 1. Buscar as 3 últimas notícias de forma segura
    ultimas_noticias = db.query(Noticia).order_by(desc(Noticia.data_publicacao)).limit(5).all()
    resultados = db.query(Noticia, Regiao).join(Regiao).order_by(desc(Noticia.data_publicacao)).limit(3).all()
    
    # 2. Total da semana atual (últimos 7 dias)
    total_hoje = db.query(Noticia).count()
    total_semana_atual = db.query(Noticia).filter(Noticia.data_publicacao >= uma_semana_atras).count()
    
    # 3. Total da semana anterior (de 14 a 7 dias atrás)
    total_semana_anterior = db.query(Noticia).filter(
        Noticia.data_publicacao >= duas_semanas_atras,
        Noticia.data_publicacao < uma_semana_atras
    ).count()

    # Média Diária (total da semana atual / 7)
    media_diaria = total_semana_atual / 7

    # Comparação percentual
    if total_semana_anterior > 0:
        crescimento = ((total_semana_atual - total_semana_anterior) / total_semana_anterior) * 100
    else:
        crescimento = 100.0 if total_semana_atual > 0 else 0.0

    return {
        "latest_news": [
        {
            "id": n.id,
            "titulo": n.titulo,
            "Portal": n.Portal,
            "data_publicacao": n.data_publicacao,
            "regiao": r.nome  # Acessando o campo da região vinculada
        } for n, r in resultados
    ],
        "total_atual": total_hoje,
        "media_diaria": round(media_diaria, 2),
        "crescimento_percentual": round(crescimento, 2),
        "total_semana": total_semana_atual
    }

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+