from sqlalchemy.orm import Session
from backend.app.models import UsuarioModel, RegiaoModel, NoticiaModel

class PostgresRepositoryAdapter:
    def __init__(self, db: Session):
        # O adaptador recebe a sessão ativa do banco de dados para trabalhar
        self.db = db

    def salvar_usuario(self, user_data: dict) -> bool:
        # 1. Transforma o dicionário vindo do FastAPI em um Objeto do banco
        novo_usuario = UsuarioModel(
            nome=user_data.get("nome"),
            email=user_data.get("email"),
            senha=user_data.get("senha")
        )
        # 2. Avisa o SQLAlchemy que queremos inserir esse objeto
        self.db.add(novo_usuario)
        # 3. Confirma a transação no PostgreSQL (executa o INSERT)
        self.db.commit()
        return True

