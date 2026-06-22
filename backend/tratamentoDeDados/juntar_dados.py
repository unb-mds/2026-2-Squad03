import json
import os
from tratamentoDeTexto import formatar_texto
#import enviar_ao_db


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

                noticia_llm['resumo_raw'] = formatar_texto(noticia_llm['resumo_raw'])
                noticia_llm['resumo_blur'] = formatar_texto(noticia_llm['resumo_blur'])

                noticia_llm.update({
                    "conteudo": formatar_texto(noticia_resultado['conteudo'])
                })
                del noticia_llm['feminicidio']
                print(noticia_llm)
                
                # enviar_ao_db(noticia_llm) # AQUI AQUI TÁ BONITNHU