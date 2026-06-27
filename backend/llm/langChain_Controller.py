from backend.llm.langChain import classifation_news_with_LLM
import json
import os
from backend.tratamentoDeDados.juntar_dados import juntar_dados

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def read_json(path):
    with open(path, 'r', encoding="utf-8") as file:
        data = json.load(file)

    return data if data else []

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def save_result_to_json(result, noticia):
    output_path = os.path.join("backend/llm/news-llm.json")

    # carrega existentes
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            try:
                news_exists = json.load(f)
            except:
                news_exists = []
    else:
        news_exists = []

    # pega url corretamente (dict)
    result_noticia_url = noticia.get("fonte_url")

    # verifica duplicação
    for news in news_exists:
        if news.get("fonte_url") == result_noticia_url:
            print("Elemento já existe no JSON.")
            return

    # adiciona e salva UMA vez
    news_exists.append(result)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(news_exists, f, ensure_ascii=False, indent=4)

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def main():
    path = os.path.join("scrapers/resultados/resultados.json")
    noticias = read_json(path)

    if noticias:
        for noticia in noticias:
            
            result = classifation_news_with_LLM(noticia)
            if result != None:
                print(result)
                save_result_to_json(result, noticia)

    juntar_dados()

if __name__ == "__main__":
    main()
    
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+