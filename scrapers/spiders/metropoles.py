import sys
import os
import platform
from urllib import response
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from playwright.sync_api import sync_playwright
from datetime import date
from datetime import datetime

# Ajuste de Fuso Horário Multiplataforma
if platform.system() == "Windows":
    try:
        import tzdata
    except ImportError:
        pass
    from zoneinfo import ZoneInfo
else:
    from zoneinfo import ZoneInfo

from backend.tratamentoDeDados.tratamentoDeTexto import transformar_padrao_data, formatar_texto, juntar_texto
from urllib.parse import urljoin

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class metropoles_spider(scrapy.Spider):
    name = 'metropoles'

    def __init__(self, urls = None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = urls or []

    def parse(self, response, **kwargs):
        data_da_publicacao = response.css('meta[property="article:published_time"]::attr(content)').get()

        if not data_da_publicacao:
            return

        hoje_brasilia = datetime.now(ZoneInfo("America/Sao_Paulo"))
        
        print("noticia: " + response.url)
        print(data_da_publicacao) 
        print(hoje_brasilia)

        dia_da_publicacao = data_da_publicacao[8:10]

        # Mantendo sua lógica original de comparação
        if(int(dia_da_publicacao) == hoje_brasilia.day): 
            print("noticia valida")

            alltext = response.css('article p *::text, article p::text').getall()

            news = juntar_texto(alltext)

            yield { 
                    'Portal': 'Metrópoles',
                    'titulo': response.css('h1::text').get(),
                    'data_publicacao': transformar_padrao_data(data_da_publicacao),
                    'fonte_url': response.url,
                    'conteudo': formatar_texto(news)
                }
            
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+
        
def play_writght():
    urls = []

    with sync_playwright() as pw:
        todas_noticias_do_dia = False

        browser = pw.firefox.launch(headless = True)
        page1 = browser.new_page()
        page2 = browser.new_page()

        page1.goto(
            "https://www.metropoles.com/tag/feminicidio",
            wait_until="load"
        )

        while not todas_noticias_do_dia:

            page1.get_by_role(
                "button",
                name="Ver mais notícias",
                exact=False
            ).click()

            page1.wait_for_timeout(2000)

            urls = page1.locator("h3 a[href]").evaluate_all(
                """
                els => [...new Set(
                    els.map(el => el.href)
                )]
                """
            )

            print(urls)
            ultima_noticia = urls[-1]

            page2.goto(ultima_noticia, wait_until="load")

            data_da_publicacao = page2.locator('meta[property="article:published_time"]').get_attribute('content')

            if not data_da_publicacao:
                return

            print(data_da_publicacao)

            dia_da_publicacao = data_da_publicacao[8:10]
            mes_da_publicacao = data_da_publicacao[5:7]

            todas_noticias_do_dia = verificar_dia_mes(dia_da_publicacao, mes_da_publicacao)

        browser.close()

    return urls

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def verificar_dia_mes(dia, mes):
    if (int(mes) == date.today().month):
        if (int(dia) < date.today().day):
            return True
        else:
            return False
    else:
        return True

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def metropoles_run_spider():
    urls = play_writght() 

    settings = get_project_settings()
    settings.set(
        'FEEDS',
        {
            'scrapers/resultados/metropoles.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True
            }
        }
    )
    settings.set('DOWNLOADER_CLIENT_TLS_VERIFY', False)
    process = CrawlerProcess(settings)
    process.crawl(metropoles_spider, urls=urls)
    process.start()