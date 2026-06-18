from langChain import classifation_news_with_LLM
import json
import os

def read_json(path):
    with open(path, 'r') as file:
        data = json.load(file)

    if data != 0:
        return data
    else:
        print("Nenhuma notícia encontrada no arquivo.")
        return None
    
def save_result_to_json(result):
    
    try:
        output_path = os.path.join("backend/llm/news-llm.json")
        if os.path.exists(output_path):
            with open(output_path, "r", encoding="utf-8") as f:
                try:
                    news_exists = json.load(f)
                except:
                    news_exists = []
        
        # Verifica se o elemento já existe
        for news in news_exists:
            if news.title == result.title:
                print("Elemento já existe no JSON.")
                return
            else:
                with open(output_path, "w", encoding="utf-8") as f:
                    news_exists.append(result)
                    json.dump(news_exists, f, ensure_ascii=False, indent=4)
                
            
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")

    except Exception as e:
        print(f"Erro inesperado: {e}")



def main():
    portais = ["g1", "metropoles", "r7", "cnn"]

    for portal in portais:
        path = os.path.join("scrapers/resultados/", f"{portal}.json")
        noticias = read_json(path)

        if noticias:
            for noticia in noticias:
                result = classifation_news_with_LLM(noticia)
                print(result)
                save_result_to_json(result)
        


if __name__ == "__main__":
    main()
