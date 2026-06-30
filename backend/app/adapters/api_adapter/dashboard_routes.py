"""
Rotas para alimentação de dados do Dashboard (Refatorado).

Este módulo fornece um endpoint consolidado que atua como o "motor analítico" 
do sistema. Ele calcula e retorna estatísticas gerais, métricas temporais, 
distribuição geográfica e participação de mercado (portais) sobre as notícias 
processadas, alimentando todos os gráficos e indicadores visuais do frontend 
em uma única requisição.

Informações Úteis:
    - Padrão de Projeto: Utiliza funções aninhadas (closures) para isolar o escopo 
      de cada métrica. Isso melhora a legibilidade do código e permite que a sessão 
      do banco (`db`) seja compartilhada implicitamente entre todas as rotinas.
    - Otimização Geoespacial: O processamento de regiões por estado/macro-região 
      utiliza Expressões Regulares (Regex) em memória para extrair as siglas UF 
      diretamente da string de nome, evitando queries complexas de geocodificação reversa.
"""

import re
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.app.database import get_db
from backend.app.models import NoticiaModel as Noticia
from backend.app.models import RegiaoModel as Regiao

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# Roteador do FastAPI dedicado aos endpoints do Dashboard.
router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# Lista auxiliar para armazenamento temporário de estatísticas (uso interno).
estatisticas = list()

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# 📱 Endpoint para o Front-end listar os locais que possuem alertas/notícias
@router.get("/")
def dashboard(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Endpoint agregador para o Dashboard analítico.

    Ao invés de realizar múltiplas requisições HTTP do frontend para cada gráfico,
    este endpoint concentra a execução de diversas queries agregadoras e devolve
    um JSON massivo com todos os dados processados e formatados.

    Args:
        db (Session, optional): Sessão do banco de dados injetada pelo FastAPI.

    Returns:
        dict: Um payload complexo contendo chaves para `latest_news`, `estatisticas`, 
        `top_portais`, `noticias_semana`, `top_regioes` e `noticias_por_estado`.
    """
    
    def get_ultimas_noticias() -> List[Dict[str, Any]]:
        """
        Recupera as 3 notícias mais recentes cadastradas no sistema.
        
        Realiza um JOIN com a tabela de Regiões para garantir que a localização 
        seja exibida no feed. Os resultados são ordenados de forma decrescente.
        """
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
    
    def get_estatisticas() -> List[Dict[str, Any]]:
        """
        Calcula as métricas chave de performance (KPIs) de volume.
        
        Compara o volume de publicações dos últimos 7 dias com o período 
        homólogo anterior (de 14 a 7 dias atrás) para calcular a taxa de crescimento.
        """
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

    def portais() -> List[Dict[str, Any]]:
        """
        Processa o Market Share dos portais de notícias rastreados.
        
        Utiliza o operador SQL `ILIKE` para realizar contagens case-insensitive
        sobre as strings do portal (ex: "G1", "g1"). Retorna os valores absolutos
        e os percentuais relativos ao total de notícias.
        """
        g1 = db.query(Noticia).filter(Noticia.Portal.ilike("g1")).count()
        cnn = db.query(Noticia).filter(Noticia.Portal.ilike("cnn")).count()
        r7 = db.query(Noticia).filter(Noticia.Portal.ilike("r7")).count()
        metropoles = db.query(Noticia).filter(Noticia.Portal.ilike("metrópoles")).count()
        
        total = db.query(Noticia).count()

        dados_brutos = [
            {"name": "G1", "value": g1},
            {"name": "CNN", "value": cnn},
            {"name": "R7", "value": r7},
            {"name": "Metrópoles", "value": metropoles}
        ]

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

    def get_noticias_por_dia_e_data() -> List[Dict[str, Any]]:
        """
        Agrupa o volume de publicações por dia para renderização de gráficos de linha/barra.
        
        Utiliza a função nativa `func.date` do banco de dados para truncar o 
        timestamp (datetime) apenas para a data (date), permitindo o agrupamento 
        (`GROUP BY`) exato das ocorrências.
        """
        # Busca os últimos 7 dias que POSSUEM notícias (independente de quão antigos sejam)
        query = db.query(
            func.date(Noticia.data_publicacao).label('data_dia'),
            func.count(Noticia.id).label('total')
        ).group_by(
            func.date(Noticia.data_publicacao)
        ).order_by(
            func.date(Noticia.data_publicacao).desc()
        ).limit(7).all()

        # Inverte para o gráfico desenhar da esquerda (antigo) para a direita (recente)
        resultados = list(reversed(query))
        
        dias_semana_map = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        
        resultado_final = []
        for data_dia, total in resultados:
            dia_nome = dias_semana_map[data_dia.weekday()]
            resultado_final.append({
                "dia": f"{dia_nome} - {data_dia.day}",
                "noticias": total
            })
            
        return resultado_final
    
    def get_noticias_por_regiao() -> List[Dict[str, Any]]:
        """
        Calcula a distribuição estatística de eventos por macro-região brasileira.
        
        Aplica uma expressão regular sobre o texto bruto do local (ex: "São Paulo, SP")
        para isolar a UF ("SP") e a categoriza dentro do dicionário de macro-regiões.
        """
        mapa_regioes = {
            'Norte': ['AM', 'RR', 'AP', 'PA', 'TO', 'RO', 'AC'],
            'Nordeste': ['MA', 'PI', 'CE', 'RN', 'PE', 'PB', 'SE', 'AL', 'BA'],
            'Centro-Oeste': ['MT', 'MS', 'GO', 'DF'],
            'Sudeste': ['SP', 'RJ', 'ES', 'MG'],
            'Sul': ['PR', 'RS', 'SC']
        }

        query = db.query(Regiao.nome).filter(Regiao.nome != None).all()
        
        contagem = {regiao: 0 for regiao in mapa_regioes}
        
        # Regex: Procura por uma vírgula, espaços opcionais, e extamente 2 letras maiúsculas no final
        regex_estado = re.compile(r',\s*([A-Z]{2})$')
        
        for row in query:
            nome_completo = row[0]
            
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
    
    def get_noticias_por_estado() -> Dict[str, int]:
        """
        Gera o mapa de calor estatístico bruto agrupado estritamente por Unidade Federativa.
        
        Reutiliza a lógica de Regex para extrair as UFs e constrói um dicionário
        simples (chave-valor) para consumo de mapas coropléticos no frontend.
        """
        regex_estado = re.compile(r',\s*([A-Z]{2})$')
        query = db.query(Regiao.nome).filter(Regiao.nome != None).all()
        
        estado_contagem = {}
        for row in query:
            match = regex_estado.search(str(row[0]))
            if match:
                uf = match.group(1).upper()
                estado_contagem[uf] = estado_contagem.get(uf, 0) + 1
                
        return estado_contagem 
    
    # Orquestra a chamada de todas as rotinas e constrói o JSON final
    return {
        "latest_news": get_ultimas_noticias(),
        "estatisticas": get_estatisticas(),
        "top_portais" : portais(),
        "noticias_semana" : get_noticias_por_dia_e_data(),
        "top_regioes" : get_noticias_por_regiao() ,
        "noticias_por_estado" : get_noticias_por_estado()
    }

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+