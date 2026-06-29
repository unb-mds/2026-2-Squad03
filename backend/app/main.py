"""
Ponto de entrada principal da API do VeritasIA.

Este módulo é o coração do backend. Ele inicializa a aplicação ASGI utilizando o FastAPI, 
orquestra a injeção de dependências, configura as políticas de segurança de rede (CORS) 
e agrega todos os roteadores de domínio (adapters/rotas) da aplicação.

Informações Úteis:
    - Arquitetura: Funciona como o controlador principal no padrão MVC/Hexagonal, 
      delegando a lógica de negócio para os roteadores específicos.
    - Segurança (CORS): Atualmente configurado em modo permissivo (wildcard *), 
      o que é excelente para desenvolvimento, mas deve ser restrito em produção.
    - Infraestrutura: A rota raiz atua como um "Health Check" avançado, validando 
      não apenas se o servidor web está no ar, mas se a infraestrutura de dados 
      está íntegra e sincronizada.
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

# Instância principal do FastAPI.
# Responsável por gerenciar o ciclo de vida da aplicação web, roteamento e middlewares.
app = FastAPI(title="VeritasIA API")

# Lista de origens seguras mapeadas.
# Nota Técnica: Embora definida, esta lista atualmente está sendo ignorada (sobrescrita) 
# pelo parâmetro allow_origins=["*"] na configuração do CORSMiddleware abaixo.
origins = [
        "https://unb-mds.github.io",
        "https://unb-mds.github.io/2026-2-VeritasIA", # Removi a barra final
        "http://localhost:5173" # Adicionei para testes locais
    ]

# Configuração de CORS para permitir requisições do frontend (local e em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: Substituir por allow_origins=origins em ambiente de Produção
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
def home() -> dict:
    """
    Rota raiz e Health Check avançado da API.

    Ao receber uma requisição GET na raiz (/), esta rota executa silenciosamente
    uma rotina de validação de infraestrutura. Ela garante que o banco de dados
    PostgreSQL está acessível, ativa recursos espaciais e sincroniza os modelos
    declarativos do SQLAlchemy com as tabelas físicas do banco.

    Returns:
        dict: Um payload JSON simples confirmando a prontidão do servidor.
    """
    
    def rodar_teste_infraestrutura() -> None:
        """
        Rotina interna de sincronização e validação de banco de dados.
        
        Esta função é responsável por realizar o provisionamento automático
        da infraestrutura de dados (Auto-Migration simplificada). É ideal para 
        ambientes de desenvolvimento e provas de conceito (PoC).

        Lógica de Execução:
            1. Renderização Segura: Obtém a string de conexão ocultando a senha.
            2. Ativação Espacial: Força a criação da extensão 'postgis'.
            3. Sincronização ORM: Instruindo o SQLAlchemy a escanear e criar as tabelas.

        Raises:
            Exception: Captura e loga falhas de conexão, evitando crash do servidor.
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