import json
import os
import httpx
import asyncio
from supabase import create_client, Client
from datetime import datetime, timezone
from geopy.geocoders import Nominatim
from geoalchemy2.elements import WKTElement
from geoalchemy2 import Geometry

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

geolocator = Nominatim(user_agent="duplicata_scraper")

async def buscar_noticia():
    url="http://127.0.0.1:8000/noticias"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"Erro ao buscar notícia: {response.status_code}")
            return None
        return response.json()

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def read_json_resultados():
    try:
        with open('scrapers/resultados/resultados.json', 'r', encoding="utf-8") as file_result:
            print("Arquivo resultados.json carregado com sucesso.")
            data_resultados = json.load(file_result)
        with open('backend/llm/news-llm.json', 'r', encoding="utf-8") as file_llm:
            print("Arquivo news-llm.json carregado com sucesso.")
            data_llm_resultados = json.load(file_llm)
        return data_resultados, data_llm_resultados
    except FileNotFoundError:
        print('Arquivo não encontrado')
    except Exception as error:
        print('Erro na incialização')

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def juntar_dados():
    dados_resultados, dados_llm = read_json_resultados()
    count = 0  # Contador para notícias inseridas

    for noticia_resultado in dados_resultados:
        for noticia_llm in dados_llm:
            resp = asyncio.run(buscar_noticia())
            try:
                if noticia_llm["fonte_url"] == resp[count]: 
                    print(resp[count])
                    print("noticia já existe no banco de dados, não será inserida novamente.")
            except Exception as e:
                print(f"Erro ao buscar notícia: {e}")
                continue  # Pula para a próxima iteração do loop

juntar_dados()

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+