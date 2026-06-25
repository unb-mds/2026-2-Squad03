## LangChain Controlador

o LangChain_Controller tem o papel principal de coletar as noticias que foram salvas da coleta do scrapy e passar para a LLM. apos isso a LLm retorna a noticia e ela é salva em um arquivo JSON: "news-llm.json"

### Formato do Arquivo Recolhido

```json
    {
        "Portal": "portal de noticia",
        "titulo": "titulo",
        "data_publicacao": "yyyy-mm-dd hh-mm-ss",
        "fonte_url": "url",
        "conteudo": "noticia"
    }
```

### Formato do Arquivo de Saida

```json
        {
        "feminicidio": "true ou False (True se for uma noticia de um feminicidio ; False caso não seja)",
        "Portal": "mantem o portal",
        "resumo_raw": "resumo completo",
        "resumo_blur": "resumo censurado",
        "local": "cidade, Estado",
        "fonte_url": "mantem o url"
    },
```

## Envio para o Banco de Dados

Para enviar para o banco de dados primeiro os resumos feitos pela LLM passa por uma tratagem de dados para polir o texto e deiar no formato esperado pelo Banco de dados, para isso utiliza-se a função "formatar_texto" aonde ela recebe o texto e remove espaços vazios, quebras de linhas, tabs e emojis.

logo apos essa tratagem e feito um cruzamento de dados para que se ache as noticias que são equivalentes tanto no "resultados.json" que vem do scrapy, quanto no "news-llm.json" que vem da llm

feita esse cruzamento de dados as informaçoes sobre a noticias são recolhidas de forma que a saida para o banco de dados fique:

```json
        {
        "Portal": "mantem o portal",
        "resumo_raw": "resumo completo",
        "resumo_blur": "resumo censurado",
        "local": "cidade, Estado",
        "fonte_url": "mantem o url",
        "conteudo": "noticia",
        "data_publicacao": "yyyy-mm-dd hh-mm-ss"
    },
```