from supabase import create_client, Client
from datetime import datetime, timezone

# 1. COLOQUE SUAS CHAVES AQUI (Pegue no painel do Supabase: Project Settings -> API)
SUPABASE_URL = "https://bbpmgljnzuxbhqncquri.supabase.co"
SUPABASE_KEY = "sb_secret_VZ7lddSu1NZlzUxGfvsPEQ_jl1ibTyo"

# Inicializa o cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. NOSSO DADO DE TESTE (Respeitando fielmente a estrutura da sua tabela)
noticia_teste = {
    "titulo": "TESTE DE INTEGRAÇÃO: Notícia Falsa sobre o Clima",
    "url": "https://teste-veritas.com/teste-01",
    "resumo_raw": "Resumo gerado mockado para testar o banco de dados.",
    "data_publicacao": datetime.now(timezone.utc).isoformat(), # Gera a data/hora atual no formato ISO
    "regiao_id": 1, # Simulando que 1 seja DF
    "resumo_blur": "Resumo ofuscado mockado para teste.",
    "corpo_texto": "Este é o corpo do texto completo extraído pelo scraper fictício. Se você está lendo isso no painel do Supabase, o teste foi um sucesso absoluto!",
    "veiculo": "Script de Teste Local"
}

def rodar_teste():
    print("⏳ Iniciando teste de conexão com o Supabase...")
    
    try:
        # Tenta inserir na tabela 'noticias'
        resposta = supabase.table("noticias").insert(noticia_teste).execute()
        
        # Se der certo, ele retorna os dados inseridos (incluindo o ID gerado pelo banco)
        if resposta.data:
            print("✅ SUCESSO! A notícia foi salva no banco de dados.")
            print(f"🆔 ID gerado no banco: {resposta.data[0]['id']}")
            print("👉 Vá até o painel do Supabase e verifique a tabela 'noticias'!")
            
    except Exception as e:
        print("\n❌ DEU ERRO:")
        print(f"Detalhes do erro: {e}")
        print("Verifique se o nome da tabela está correto, se as chaves são válidas e se a coluna regiao_id não está ferindo a Foreign Key (o ID 1 precisa existir na tabela regioes_monitoradas).")

if __name__ == "__main__":
    rodar_teste()