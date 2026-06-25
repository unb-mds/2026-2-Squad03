O LangChain é um framework de código aberto que facilita a criação de aplicativos usando Grandes Modelos de Linguagem (LLMs), como o GPT, Claude, DeepSeak, entre outros.

# Utilidade para o VeritasIA

Para o projeto, LangChain está sendo utilizado após o fim da execução do `workflow: executar-scrapy` [**Clique aqui para ler**](https://unb-mds.github.io/2026-2-VeritasIA/backend/scrapy/Automacao/). 

O FrameWork, LangChain, tem como utilidade realizar tarefas, como:

- Verificação de coêrencia das notícias
    - Mesmo com os filtros que há dentro dos portais, vários deles contém nóticias erroneas, dessa forma, a LLM lê todas as nóticias e faz uma verificação se ela condiz com `A Lei do Feminicídio (Lei n.º 13.104/2015)`
- Resumos sobre a notícia
    - O projeto tem ciência que todas as notícias coletadas possuem auditoria, dessa forma, para não usufruir do trabalho de terceiros fazemos um resumo da notícia, e essa é disponibilizada dentro da nossa aplicação, o URL da notícia primaria também é disponibilizado. 

## Como funciona?

Dentro da nossa aplicação é criado um arquivo chamado de `LangChain.py`, onde inicializamos o modelo que queremos usufruir da LLM, em nosso caso:

``` python
model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
```

Criamos um Prompt baseado no que desejamos que a LLM extraia de dentro da notícia:

``` python
system1 = """
    Você é um classificador de notícias.

    Analise a notícia e determine se ela se enquadra na Lei do Feminicídio (Lei 13.104/2015).

    Considere feminicídio somente quando houver indícios claros de:
    - violência doméstica e familiar contra a mulher;
    - menosprezo à condição de mulher;
    - discriminação de gênero.

    Retorne exclusivamente um JSON válido:

    {{
        "feminicidio": true ou false,
        "title": "...",
        "resumo": "...",
        "local": "Estado"
    }}

    Se alguma informação não estiver disponível, utilize "Não Encontrado".
    Não escreva explicações adicionais.
    """
```


Agora é utilizando algumas funcionalidades de dentro do próprio LangChain para realizar o envio do prompt e a resposta:

``` python
1. parser = StrOutputParser() # transformando a resposda em string

2.  prompt = ChatPromptTemplate.from_messages([ # Criando um template de prompt
3.      ("system", system1),
4.      ("user", "{news}")
5.  ])

6.    structured_model = model.with_structured_output(NewsClassification)

7.  chain = prompt | model | parser | structured_model

8.  response = chain.invoke({"news": news})


9. return response.model_dump()
```

1- Na primeira linha, estamos transformando a resposta que será enviada pelo `Gemini` como uma String.
2- Criamos o template do prompt, enviando o contexto para a LLM e inicializando o `user`.
6- Criamos um modelo Base de como queremos o retorno:
``` python
from pydantic import BaseModel

class NewsClassification(BaseModel):
    feminicidio: str
    title: str
    resumo: str
    local: str
```
7- Inicializamos tudo para invocarmos a resposta, como: `prompt`, `modelo da LLM`, `parse` e o `modelo Base de retorno`.
8-  Por fim, invocamos a resposta passando a nóticia que queremos que seja analisada.
9. Retorna a notícia para nosso `LangChainController` [**Clique aqui para ler**](https://unb-mds.github.io/2026-2-VeritasIA/backend/langChain/LangChainControlador/)
