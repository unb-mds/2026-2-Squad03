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

    def salvar_local(self, nome: str, latitude: float, longitude: float) -> RegiaoModel:
        nova_regiao = RegiaoModel(nome=nome, latitude=latitude, longitude=longitude)
        self.db.add(nova_regiao)
        self.db.commit()
        # O refresh atualiza o objeto com o ID que o Postgres gerou automaticamente
        self.db.refresh(nova_regiao)
        return nova_regiao

    def listar_todas_regioes(self):
        # Equivalente ao 'SELECT * FROM regioes_monitoradas'
        return self.db.query(RegiaoModel).all()

    def salvar_noticia(self, titulo: str, url: str, resumo: str, sentimento: str, regiao_id: int):
        nova_noticia = NoticiaModel(
            titulo=titulo,
            url=url,
            resumo=resumo,
            sentimento=sentimento,
            regiao_id=regiao_id
        )
        self.db.add(nova_noticia)
        self.db.commit()
        return True