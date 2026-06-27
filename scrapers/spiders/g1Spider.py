import sys
import os
import platform
from datetime import datetime, date

# Adiciona a pasta raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from playwright.sync_api import sync_playwright

# Ajuste de Fuso Horário Multiplataforma
if platform.system() == "Windows":
    try:
        import tzdata
    except ImportError:
        print("Aviso: Pacote 'tzdata' não instalado. Instale com 'pip install tzdata'")
    from zoneinfo import ZoneInfo
else:
    from zoneinfo import ZoneInfo

from backend.tratamentoDeDados.tratamentoDeTexto import transformar_padrao_data, formatar_texto, juntar_texto

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class g1_spider(scrapy.Spider):
    name = 'g1'

    def __init__(self, urls=None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = urls or []

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

    def parse(self, response, **kwargs):
        # Acesso seguro ao atributo datetime
        data_tag = response.css('time').attrib.get('datetime')
        if not data_tag:
            return

        # Ajuste para garantir que ZoneInfo funcione em ambos os SOs
        hoje_brasilia = datetime.now(ZoneInfo("America/Sao_Paulo"))
        
        # Ajuste de slicing se o formato for ISO (ex: 2026-06-26T...)
        dia_da_publicacao = int(data_tag[8:10])

        if dia_da_publicacao == hoje_brasilia.day:
            print("noticia valida")
            alltext = response.css('article p *::text, article p::text').getall()
            news = juntar_texto(alltext)
            
            yield { 
                    'Portal': 'G1',
                    'titulo': response.css('.content-head__title::text').get(),
                    'data_publicacao': transformar_padrao_data(data_tag),
                    'fonte_url': response.url,
                    'conteudo': formatar_texto(news)
                }

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+
        
def play_writght():
    urls = []
    with sync_playwright() as pw:
        # Modo 'headed' pode ser útil para debug no Windows, mas headless=True é padrão
        browser = pw.firefox.launch(headless=True)
        page1 = browser.new_page()
        
        page1.goto("https://g1.globo.com/busca/?q=feminicidio", wait_until='load')
        page1.locator("a").filter(has_text="Filtrar por Data").click()
        page1.locator('span[data-date = "now-1d"]').click()

        scroll_to_absolute_bottom(page1)

        newsContent = page1.locator('[class = widget--info__text-container] > a').all()
        for news in newsContent:
            href = news.get_attribute("href")
            if href:
                urls.append(href)
        
        browser.close()
    return urls

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def scroll_to_absolute_bottom(page):
    while True:
        current_height = page.evaluate("document.body.scrollHeight")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000) 
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == current_height:
            break

def g1_run_spider():
    urls = play_writght() 
    if not urls:
        print("Nenhuma URL encontrada.")
        return

    settings = get_project_settings()
    settings.set('FEEDS', {
        'scrapers/resultados/g1.json': {
            'format': 'json',
            'encoding': 'utf-8',
            'overwrite': True
        }
    })
    process = CrawlerProcess(settings)
    process.crawl(g1_spider, urls=urls)
    process.start()