"""
Schemas de serialização de dados (Pydantic) para Notícias e Regiões.

Este módulo define os Modelos de Transferência de Dados (DTOs) utilizados 
pela API para formatar as respostas HTTP. Ele utiliza o conceito de 
"Nested Schemas" (Schemas Aninhados) para construir payloads JSON ricos, 
permitindo que o frontend receba os dados da Notícia já com os dados da 
Região embutidos em uma única requisição.

Informações Úteis:
    - Tipagem Moderna: Utiliza a sintaxe `str | None` nativa do Python 3.10+ 
      para definir campos opcionais de forma mais limpa.
    - Serialização ORM: A configuração `from_attributes = True` instrui o 
      Pydantic a ler os dados não apenas de dicionários, mas diretamente de 
      objetos do SQLAlchemy, resolvendo automaticamente os relacionamentos (`relationship`).
"""

from pydantic import BaseModel
from datetime import datetime

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class RegiaoParcialResponse(BaseModel):
    """
    Schema parcial para representação de uma Região.

    Atua como um sub-modelo (nested model) para ser embutido dentro da resposta 
    de Notícias. Ele contém apenas os dados essenciais da região, evitando 
    sobrecarga de dados (over-fetching) ou problemas de dependência circular.

    Attributes:
        id (int): Identificador único da região no banco de dados.
        nome (str): Nome por extenso da região monitorada.
        sigla (str | None): Sigla representativa da região (ex: "DF"). É um 
            campo opcional, retornando `null` no JSON caso não esteja preenchido.
    """
    id: int
    nome: str
    sigla: str | None = None

    class Config:
        """
        Configurações internas do modelo Pydantic.
        
        Atributos:
            from_attributes (bool): Habilita o mapeamento direto de atributos de 
                instâncias de classes (como os modelos do SQLAlchemy). Substitui 
                o antigo `orm_mode = True` utilizado no Pydantic v1.
        """
        from_attributes = True 

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class NoticiaResponse(BaseModel):
    """
    Schema principal de resposta para a entidade Notícia.

    Define a estrutura exata do payload JSON que será devolvido ao cliente (frontend).
    Além de expor os dados básicos da notícia, mapeia o relacionamento com a 
    tabela de regiões, gerando uma estrutura hierárquica no JSON.

    Attributes:
        id (int): Chave primária da notícia.
        titulo (str): Título ou manchete original.
        resumo_blur (str): Versão do resumo processada com filtros sensíveis/anonimizada.
        resumo_raw (str): Versão bruta do resumo gerado pela IA.
        Portal (str): Nome do veículo de imprensa fonte da notícia.
        fonte_url (str): URL direta para a publicação original.
        data_publicacao (datetime): Carimbo de tempo do momento da publicação.
        regiao_id (int): Chave estrangeira referenciando o ID da região associada.
        regiao (RegiaoParcialResponse | None): Objeto aninhado contendo os dados 
            da região. O Pydantic resolve isso automaticamente se o modelo SQLAlchemy 
            tiver o atributo `regiao` carregado (via `joinedload` ou `lazy='select'`).
    """
    id: int
    titulo: str
    resumo_blur: str 
    resumo_raw: str 
    Portal: str
    fonte_url: str
    data_publicacao: datetime
    regiao_id: int
    regiao: RegiaoParcialResponse | None = None 

    class Config:
        """
        Configurações internas do modelo Pydantic.
        
        Atributos:
            from_attributes (bool): Permite a serialização transparente dos 
                modelos ORM do SQLAlchemy para este schema Pydantic.
        """
        from_attributes = True

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+