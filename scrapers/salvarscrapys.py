import json
import glob
import os

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def salvar_todos_resultados():
    todas_noticias = []
    try:
        # Ler resultados já existentes
        arquivo_final = "scrapers/resultados/resultados.json"
        if os.path.exists(arquivo_final):
            with open(arquivo_final, "r", encoding="utf-8") as f:
                try:
                    todas_noticias = json.load(f)
                except:
                    todas_noticias = []
        # Ler novos arquivos
        for arquivo_json in glob.glob("scrapers/resultados/*.json"):
            if arquivo_json.endswith("resultados.json"):
                continue
            with open(arquivo_json, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if isinstance(dados, list):
                    todas_noticias.extend(dados)
                else:
                    todas_noticias.append(dados)
        # Remove duplicados (opcional)
        noticias_unicas = []
        vistos = set()
        for noticia in todas_noticias:
            texto = json.dumps(noticia, sort_keys=True)
            if texto not in vistos:
                vistos.add(texto)
                noticias_unicas.append(noticia)
        # Salvar tudo
        with open(arquivo_final, "w", encoding="utf-8") as f:
            json.dump(noticias_unicas, f, ensure_ascii=False, indent=4)

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")

    except Exception as e:
        print(f"Erro inesperado: {e}")

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+