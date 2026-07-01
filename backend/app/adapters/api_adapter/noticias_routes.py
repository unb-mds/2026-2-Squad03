"""
Rotas para listagem e consulta detalhada de notícias.

Este módulo concentra os endpoints da API responsáveis por expor o acervo de 
notícias extraídas e processadas pelo VeritasIA. Ele atua como a interface 
principal para o frontend renderizar o feed de alertas e buscar os detalhes 
individuais de cada evento.

Informações Úteis:
    - Otimização de Performance: A rota de listagem utiliza "Eager Loading" 
      (carregamento antecipado) através do `joinedload` do SQLAlchemy. Isso 
      garante que a API busque as notícias e suas respectivas regiões em uma 
      única query SQL (usando JOIN), otimizando drasticamente o tempo de resposta.
    - Tratamento de Exceções: A rota de busca individual padroniza o retorno 
      de erros HTTP 404 para recursos inexistentes, facilitando o tratamento 
      de estado no frontend (ex: exibição de página "Not Found").
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Any, Dict
from backend.app.database import get_db
from backend.app.models import NoticiaModel as Noticia
from backend.app.models import RegiaoModel as Regiao
from backend.app.schemas.noticia import NoticiaResponse

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# Roteador do FastAPI dedicado aos endpoints de notícias.
# O `prefix="/noticias"` garante que todas as rotas neste arquivo comecem com este caminho.
# A `tags=["Locais e Notícias"]` organiza e agrupa visualmente esses endpoints na documentação interativa (Swagger UI).
router = APIRouter(
    prefix="/noticias",
    tags=["Locais e Notícias"]
)

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# 📱 Endpoint para o Front-end listar os locais que possuem alertas/notícias
@router.get("/", response_model=List[NoticiaResponse])
def listar_noticias_locais(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Lista as notícias cadastradas no banco de dados com suporte a paginação 
    e inclusão automática dos dados espaciais (Região).

    Este endpoint recupera um lote de notícias trazendo as propriedades do modelo
    de Região embutidas (nested). A utilização do `.options(joinedload(...))` 
    resolve o problema do N+1, onde o ORM faria uma nova consulta ao banco para 
    cada notícia listada apenas para descobrir a sua região.

    Variáveis de Escopo:
        noticias (List[Noticia]): Armazena o resultado da query ORM executada no banco.

    Args:
        skip (int, optional): Número de registros a serem ignorados no início da 
            busca (Offset). Utilizado para paginação infinita no frontend. Padrão é 0.
        db (Session, optional): Sessão ativa de conexão com o banco de dados, 
            injetada via `Depends()` do FastAPI.

    Returns:
        List[NoticiaResponse]: Uma lista de objetos de Notícia, serializada 
        automaticamente pelo Pydantic, contendo os dados da região aninhados.
    """
    # O .options(joinedload(Noticia.regiao)) anexa os dados da tabela Regiao dentro do objeto Noticia
    # de forma proativa (Eager Load) na mesma transação SQL.
    noticias = (
        db.query(Noticia)
        .options(joinedload(Noticia.regiao)) 
        .all()
    )
    
    return noticias

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

@router.get("/{id}", response_model=NoticiaResponse)
def ler_noticia(id: int, db: Session = Depends(get_db)) -> Noticia:
    """
    Busca e retorna os detalhes granulares de uma notícia específica.

    Procura no banco de dados o registro exato correspondente ao `id` passado 
    como parâmetro de rota (Path Parameter). Utiliza o método `.first()` do 
    SQLAlchemy que otimiza a busca limitando o retorno ao primeiro match encontrado.

    Variáveis de Escopo:
        id (int): Extraído automaticamente da URL pelo FastAPI (ex: /noticias/5).
        noticia (Noticia | None): O objeto ORM correspondente caso encontrado, ou None.

    Args:
        id (int): O identificador primário (Primary Key) da notícia solicitada.
        db (Session, optional): Sessão do banco de dados injetada via Injeção 
            de Dependência.

    Raises:
        HTTPException: Dispara proativamente um erro HTTP 404 (Not Found) com 
            uma mensagem descritiva caso a variável `noticia` retorne None.

    Returns:
        NoticiaResponse: Os dados completos do evento serializados para envio ao cliente.
    """
    print(f"Buscando notícia com ID {id} no banco de dados...")
    
    # Executa a query filtrando estritamente pela Primary Key (id)
    noticia = db.query(Noticia).filter(Noticia.id == id).first()
    
    print(noticia, "Notícia encontrada no banco de dados")
    
    # Validação de existência para garantir integridade na resposta HTTP
    if not noticia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Notícia não encontrada"
        )
    
    return noticia

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+