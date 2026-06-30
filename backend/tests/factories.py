"""
Funções fábrica (Factories) para criação de entidades de teste.

Fornece instâncias falsas de objetos ORM (`NoticiaModel`, `RegiaoModel`) para 
serem usadas nas respostas dos mocks de banco de dados, garantindo que o 
Pydantic consiga serializar os dados corretamente.
"""

from datetime import datetime
from types import SimpleNamespace

def fake_noticia(**overrides):
    """
    Gera um objeto simulando um NoticiaModel (ORM) preenchido.
    """
    base = dict(
        id=1,
        titulo="Assalto em via pública",
        fonte_url="https://exemplo.com/noticia-1",
        conteudo="Conteúdo integral da notícia.",
        resumo_raw="Resumo bruto gerado pela IA.",
        resumo_blur="Resumo anonimizado.",
        data_publicacao=datetime(2026, 1, 1, 12, 0, 0),
        Portal="G1",
        data_no_banco=datetime(2026, 1, 1, 12, 5, 0),
        regiao_id=1,
        regiao=None,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def fake_regiao(**overrides):
    """
    Gera um objeto simulando um RegiaoModel (ORM) preenchido.
    """
    base = dict(id=1, nome="São Paulo, SP", geom=None)
    base.update(overrides)
    return SimpleNamespace(**base)