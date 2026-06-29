import re


"""
Rotas para alimentação de dados do Dashboard.

Este módulo fornece os endpoints necessários para calcular e retornar 
estatísticas gerais e métricas sobre as notícias processadas pelo sistema, 
alimentando os gráficos e indicadores visuais do frontend.
"""
from sqlalchemy import func
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
def dashboard(db: Session = Depends(get_db)):
    """
    Dashboard reestruturado com funções auxiliares para melhor legibilidade.
    """
    
    def get_ultimas_noticias():
        # Consultamos apenas uma vez para o que precisamos
        resultados = db.query(Noticia, Regiao).join(Regiao).order_by(desc(Noticia.data_publicacao)).limit(3).all()
        return [
            {
                "id": n.id,
                "titulo": n.titulo,
                "Portal": n.Portal,
                "data_publicacao": n.data_publicacao,
                "regiao": r.nome
            } for n, r in resultados
        ]
    
    def get_estatisticas():
        agora = datetime.now()
        uma_semana_atras = agora - timedelta(days=7)
        duas_semanas_atras = agora - timedelta(days=14)

        total_hoje = db.query(Noticia).count()
        total_semana_atual = db.query(Noticia).filter(Noticia.data_publicacao >= uma_semana_atras).count()
        
        total_semana_anterior = db.query(Noticia).filter(
            Noticia.data_publicacao >= duas_semanas_atras,
            Noticia.data_publicacao < uma_semana_atras
        ).count()

        media_diaria = total_semana_atual / 7 if total_semana_atual > 0 else 0
        crescimento = (((total_semana_atual - total_semana_anterior) / total_semana_anterior) * 100) if total_semana_anterior > 0 else (100.0 if total_semana_atual > 0 else 0.0)
        
        return [
            {
            "total_atual": total_hoje,
            "media_diaria": round(media_diaria, 2),
            "crescimento_percentual": round(crescimento, 2),
            "total_semana": total_semana_atual
            }
        ]

    def portais():
        # 1. Obter as contagens
        g1 = db.query(Noticia).filter(Noticia.Portal.ilike("g1")).count()
        cnn = db.query(Noticia).filter(Noticia.Portal.ilike("cnn")).count()
        r7 = db.query(Noticia).filter(Noticia.Portal.ilike("r7")).count()
        metropoles = db.query(Noticia).filter(Noticia.Portal.ilike("metrópoles")).count()
        
        total = db.query(Noticia).count()

        # 2. Definir a estrutura auxiliar para processar os dados
        dados_brutos = [
            {"name": "G1", "value": g1},
            {"name": "CNN", "value": cnn},
            {"name": "R7", "value": r7},
            {"name": "Metrópoles", "value": metropoles}
        ]

        # 3. Calcular a porcentagem dinamicamente
        resultado = []
        for item in dados_brutos:
            # Evita divisão por zero caso o banco esteja vazio
            percentual = (item["value"] / total * 100) if total > 0 else 0
            
            resultado.append({
                "name": item["name"],
                "value": item["value"],
                "percent": round(percentual, 2)
            })

        return resultado

    def get_noticias_por_dia_e_data():
        # 1. Busca os últimos 7 dias que POSSUEM notícias (independente de quão antigos sejam)
        # Isso evita o problema de retornar lista vazia se não houver notícias recentes
        query = db.query(
            func.date(Noticia.data_publicacao).label('data_dia'),
            func.count(Noticia.id).label('total')
        ).group_by(
            func.date(Noticia.data_publicacao)
        ).order_by(
            func.date(Noticia.data_publicacao).desc()
        ).limit(7).all()

        # O query retorna [ (data, count), ... ] do mais recente para o mais antigo
        # Vamos inverter para o gráfico (do mais antigo para o mais recente)
        resultados = list(reversed(query))
        
        # 2. Mapeamento simples
        dias_semana_map = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        
        resultado_final = []
        for data_dia, total in resultados:
            # data_dia aqui já é um objeto date (devido ao func.date)
            dia_nome = dias_semana_map[data_dia.weekday()]
            
            resultado_final.append({
                "dia": f"{dia_nome} - {data_dia.day}",
                "noticias": total
            })
            
        return resultado_final
    
    def get_noticias_por_regiao():
        mapa_regioes = {
        'Norte': ['AM', 'RR', 'AP', 'PA', 'TO', 'RO', 'AC'],
        'Nordeste': ['MA', 'PI', 'CE', 'RN', 'PE', 'PB', 'SE', 'AL', 'BA'],
        'Centro-Oeste': ['MT', 'MS', 'GO', 'DF'],
        'Sudeste': ['SP', 'RJ', 'ES', 'MG'],
        'Sul': ['PR', 'RS', 'SC']
        }

        # 1. Buscamos a coluna 'nome' diretamente
        # O filtro != None garante que ignoramos registros vazios ou corrompidos
        query = db.query(Regiao.nome).filter(Regiao.nome != None).all()
        
        contagem = {regiao: 0 for regiao in mapa_regioes}
        regex_estado = re.compile(r',\s*([A-Z]{2})$')
        
        for row in query:
            nome_completo = row[0]
            
            # Se por acaso vier um booleano, ignoramos
            if not isinstance(nome_completo, str):
                continue
                
            match = regex_estado.search(nome_completo)
            if match:
                sigla = match.group(1).upper()
                for regiao, estados in mapa_regioes.items():
                    if sigla in estados:
                        contagem[regiao] += 1
                        break
        
        total_geral = sum(contagem.values()) or 1
        
        return [
            {
                "name": nome,
                "value": valor,
                "percent": f"{round((valor / total_geral) * 100)}%"
            }
            for nome, valor in contagem.items()
        ]
    
    def get_noticias_por_estado():
        # Regex para capturar a sigla do estado
        regex_estado = re.compile(r',\s*([A-Z]{2})$')
        
        query = db.query(Regiao.nome).filter(Regiao.nome != None).all()
        
        estado_contagem = {}
        for row in query:
            match = regex_estado.search(str(row[0]))
            if match:
                uf = match.group(1).upper()
                estado_contagem[uf] = estado_contagem.get(uf, 0) + 1
                
        return estado_contagem # Retorna { 'SP': 50, 'RJ': 20, ... }
    
    
    return {
        "latest_news": get_ultimas_noticias(),
        "estatisticas": get_estatisticas(),
        "top_portais" : portais(),
        "noticias_semana" : get_noticias_por_dia_e_data(),
        "top_regioes" : get_noticias_por_regiao() ,
        "noticias_por_estado" : get_noticias_por_estado()
    }

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+