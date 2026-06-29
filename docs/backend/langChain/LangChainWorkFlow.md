O workflow da LLM é executado ao fim da execução do `GitHub-Aciton: executor-scraper` [**Clique aqui para ler**](https://unb-mds.github.io/2026-2-VeritasIA/backend/scrapy/Automacao/) 

## Dependências

> pip install -r backend/llm/requirements.txt

Arquivo requeriments.txt:

```json
    langchain
    python-dotenv
    langchain-google-genai
    google-api-core
    emoji
    geopy
    geoalchemy2
```

## Chaves da LLM

Para executar a LLM é necessario possuir as chaves da API, no nosso caso, `GEMINI KEY`. 

As chaves estão sendo passadas dentro do .Yamal, por meio das variáveis:

```python
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
          GOOGLE_API_KEY_1: ${{ secrets.GOOGLE_API_KEY_1 }}
          GOOGLE_API_KEY_2: ${{ secrets.GOOGLE_API_KEY_2 }}
```
Essas variáveis `Secrets` são privadas e adicionadas dentro do repositório do GitHub, nelas contém chaves de API pessoal.
