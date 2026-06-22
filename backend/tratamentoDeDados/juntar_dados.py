import json
import os
from backend.tratamentoDeDados.tratamentoDeTexto import formatar_texto
from supabase import create_client, Client
from datetime import datetime, timezone
from geopy.geocoders import Nominatim

from geoalchemy2.elements import WKTElement
from geoalchemy2 import Geometry


# 1. COLOQUE SUAS CHAVES AQUI (Pegue no painel do Supabase: Project Settings -> API)
SUPABASE_URL = "https://bbpmgljnzuxbhqncquri.supabase.co"
SUPABASE_KEY = "sb_secret_VZ7lddSu1NZlzUxGfvsPEQ_jl1ibTyo"

# Inicializa o cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

geolocator = Nominatim(user_agent="veritas_ia_bot")




def read_json_resultados():
    try:
        with open('scrapers/resultados/resultados.json', 'r', encoding="utf-8") as file_result:
            data_resultados = json.load(file_result)
        with open('backend/llm/news-llm.json', 'r', encoding="utf-8") as file_llm:
            data_llm_resultados = json.load(file_llm)
        return data_resultados, data_llm_resultados
    except FileNotFoundError:
        print('Arquivo não encontrado')
    except Exception as error:
        print('Erro na incialização')


def juntar_dados():
    dados_resultados, dados_llm = read_json_resultados()
    
    for noticia_resultado in dados_resultados:
        for noticia_llm in dados_llm:

            if noticia_llm.get('feminicidio') and noticia_llm['fonte_url'] == noticia_resultado['fonte_url']:

                # --- ADICIONE ESTA LINHA ---
                noticia_llm['data_publicacao'] = noticia_resultado.get('data_publicacao')
                noticia_llm['titulo'] = noticia_resultado.get('titulo')
                # ---------------------------

                noticia_llm['resumo_raw'] = formatar_texto(noticia_llm['resumo_raw'])
                noticia_llm['resumo_blur'] = formatar_texto(noticia_llm['resumo_blur'])

                noticia_llm.update({
                    "conteudo": formatar_texto(noticia_resultado['conteudo'])
                })
                
                del noticia_llm['feminicidio']
                
                print(noticia_llm['local'], "Local antes da geolocalização")
                
                noticia_llm['regiao_id'] = None
                
###############################################################

                # Tratando a localização
                # ... dentro do loop, após encontrar a correspondência (if...)

                # 1. Primeiro: Geolocaliza e salva a Região
                localizacao = geolocator.geocode(noticia_llm['local'])
                point_wkt = f'POINT({localizacao.longitude} {localizacao.latitude})' if localizacao else None
                dict_local = {"nome": noticia_llm['local'], "geom": point_wkt}

                try:
                    # Insere a região e captura o ID gerado pelo banco
                    res_regiao = supabase.table("regioes_monitoradas").insert(dict_local).execute()
                    novo_id_regiao = res_regiao.data[0]['id']
                    print(f"✅ Região salva com ID: {novo_id_regiao}")
                    
                    # 2. Agora: Atualiza o dicionário da notícia com o ID correto
                    noticia_llm['regiao_id'] = novo_id_regiao
                    noticia_llm.pop('local', None) 
                    
                    # 3. Finalmente: Insere a notícia
                    resposta = supabase.table("noticias").insert(noticia_llm).execute()
                    
                    if resposta.data:
                        print("✅ SUCESSO! A notícia foi salva no banco de dados.")
                        print(f"🆔 ID gerado no banco: {resposta.data[0]['id']}")

                except Exception as e:
                    print(f"Erro na transação de salvamento: {e}")


juntar_dados()