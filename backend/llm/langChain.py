from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from news_Classification import NewsClassification

def classifation_news_with_LLM(news):

    load_dotenv() # carregando arquivo .env aonde esta a "API_KEY"

    model = ChatGoogleGenerativeAI( # Configurando o modelo Do gemini
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


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

    parser = StrOutputParser() # transformando a resposda em string

    prompt = ChatPromptTemplate.from_messages([ # Criando um template de prompt
        ("system", system1),
        ("user", "{news}")
    ])

    structured_model = model.with_structured_output(NewsClassification)

    chain = prompt | model | parser | structured_model

    response = chain.invoke({"news": news})


    return response.model_dump()