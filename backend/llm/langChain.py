from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from google.api_core.exceptions import ResourceExhausted
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from backend.llm.news_Classification import NewsClassification

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def classifation_news_with_LLM(news):

    load_dotenv() # carregando arquivo .env aonde esta a "API_KEY"

    key1 = os.getenv("GOOGLE_API_KEY")
    key2 = os.getenv("GOOGLE_API_KEY_1")
    key3 = os.getenv("GOOGLE_API_KEY_2")

    minhas_keys = [key1, key2, key3]
    
    for index in range(len(minhas_keys)):
        print(minhas_keys[index])
        try:
            model = ChatGoogleGenerativeAI( # Configurando o modelo Do gemini
                model="gemini-2.5-flash",
                google_api_key=minhas_keys[index]
            )


            system1 = """
            Você é um resumidor de notícias.

            Passo 1:

            Analise a notícia e determine se ela se enquadra na Lei do Feminicídio (Lei 13.104/2015).

            Considere feminicídio somente quando houver indícios claros de:
            - violência doméstica e familiar contra a mulher;
            - menosprezo à condição de mulher;
            - discriminação de gênero.
            
            Passo 2:

            Caso a analise feita não se enquadra na Lei sobre Feminicídio, "feminicidio": False.

            se não, "feminicidio": True.

            Passo 3:

            Gere Dois resumos um "resumo_raw" e um "resumo_blur"

            "resumo_raw" = um resumo focado em extrair quem, o quê, onde, quando e por quê em no máximo 3 parágrafos).
            "resumo_blur" = indentificar gatilhos sensíveis, desarmar o tom inflamatório e substituir termos tóxicos por descrições neutras, ex: substituir xingamentos por [termo ofensivo]).

            Passo 4:
            
            Retorne exclusivamente um JSON válido:

            {{
                "titulo": "Manter o título da notícia",
                "feminicidio": True/False
                "Portal": "Manter o portal da notícia'
                "resumo_raw": "Resumo Completo",
                "resumo_blur": "Resumo com ofuscação/anonimização",
                "fonte_url": "Manter o Url da notícia"
                "local": "Região e Estado" ("caso não encontar região manter apenas Estado")
            }}

            Exemplo de saida:

            {{
                "local": "Sertãozinho, SP"
            }}


            Se alguma informação não estiver disponível, utilize "None".
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
        
        except (ResourceExhausted, ChatGoogleGenerativeAIError) as e:
            print(f"Chave {index} falhou: {e}")
            continue
        
    raise Exception("Todas as chaves de API falharam ou estão sem tokens.")

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+