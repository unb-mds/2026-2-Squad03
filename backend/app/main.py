"""
Ponto de entrada principal da API do VeritasIA.

Este módulo inicializa a aplicação FastAPI, configura os middlewares de CORS 
para permitir a comunicação com o frontend, registra os roteadores da aplicação 
(notícias, mapa, autenticação e dashboard) e define a rota raiz que executa 
um teste de conectividade e sincronização com o banco de dados.
"""

import os
from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importações do banco de dados e modelos
from backend.app.database import engine, Base
import backend.app.models as models

# Importações das rotas
from backend.app.adapters.api_adapter import auth_routes, noticias_routes, mapa_routes, dashboard_routes

app = FastAPI(title="VeritasIA API")
"""
Instância principal do FastAPI.
Responsável por orquestrar rotas, middlewares e configurações da API.
"""

# Configuração de CORS para permitir requisições do frontend (local e em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://two026-2-veritasia.onrender.com/"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# Registro de Rotas (Routers)
app.include_router(noticias_routes.router)
app.include_router(mapa_routes.router)
app.include_router(auth_routes.router)
app.include_router(dashboard_routes.router)

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

@app.get("/")
def home():
    """
    Rota raiz da API do VeritasIA.

    Ao ser acessada, esta rota executa um teste interno de infraestrutura 
    para validar a conexão com o banco de dados (Supabase), ativar a extensão 
    PostGIS (se necessário) e sincronizar os modelos ORM criando as tabelas 
    faltantes.

    Returns:
        dict: Um dicionário de boas-vindas confirmando que a API está no ar.
    """
    
    def rodar_teste_infraestrutura():
        """
        Função auxiliar interna que realiza a verificação de saúde do banco de dados.
        
        Executa os seguintes passos:
        1. Renderiza e exibe a URL de conexão (ocultando a senha por segurança).
        2. Tenta conectar ao banco de dados usando a `engine` do SQLAlchemy.
        3. Executa a criação da extensão PostGIS no PostgreSQL.
        4. Sincroniza os modelos do sistema (`Base.metadata.create_all`).
        5. Imprime logs no terminal detalhando o sucesso ou falha das operações.
        """
        print("\n" + "="*50)
        print("🔄 [VeritasIA] Iniciando teste de conexão com o Supabase...")
        print("="*50 + "\n")

        # Mostra qual URL o motor (engine) configurado no database.py está usando
        # O render_as_string(hide_password=True) protege sua senha de aparecer no terminal
        url_configurada = engine.url.render_as_string(hide_password=True)
        print(f"🔗 URL que o Python está tentando usar:\n👉 {url_configurada}\n")

        try:
            # Teste 1: Validação de Conexão e Ativação do PostGIS
            print("📡 Passo 1: Testando canal de rede e autenticação...")
            with engine.connect() as conexao:
                # Executa uma query leve para testar a saúde do banco e ativa o PostGIS
                conexao.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
                conexao.commit()
                print("✅ Sucesso! Conexão estabelecida e extensão PostGIS verificada.")

            # Teste 2: Mapeamento ORM e Criação de Tabelas Reais na Nuvem
            print("\n🔨 Passo 2: Sincronizando modelos com o banco de dados...")
            print("🔄 Criando tabelas (usuarios, regioes_monitoradas, noticias)...")
            
            # O SQLAlchemy olha para o seu models.py e cria fisicamente as tabelas se não existirem
            Base.metadata.create_all(bind=engine)
            
            print("🚀 Sucesso absoluto! Todas as tabelas foram geradas no Supabase.")
            print("\n" + "="*50)
            print("🎉 STATUS: Seu backend está PRONTO para salvar dados na nuvem!")
            print("="*50 + "\n")

        except Exception as e:
            print("\n❌ OCORREU UM ERRO DURANTE O TESTE:")
            print("-" * 50)
            print(str(e))
            print("-" * 50)
            print("💡 Dica: Verifique se o host do Session Pooler e a senha estão batendo.")
            print("="*50 + "\n")

    rodar_teste_infraestrutura()
    return {"message": "Bem-vindo a API do VeritasIA!"}

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+