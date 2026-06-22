import os
from sqlalchemy import text
from backend.app.database import engine, Base
# Garante que o SQLAlchemy carregue as classes antes de tentar criar as tabelas
import backend.app.models

def rodar_teste_infraestrutura():
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

if __name__ == "__main__":
    rodar_teste_infraestrutura()