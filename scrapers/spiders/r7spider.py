import sys
import os
import platform
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from playwright.sync_api import sync_playwright
import time
import json
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

# Adiciona a pasta raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.tratamentoDeDados.tratamentoDeTexto import formatar_texto, juntar_texto, transformar_padrao_data

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class r7_spider(scrapy.Spider):
    name = 'r7'

    def __init__(self, urls = None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = urls or []

    def parse(self, response, **kwargs):
        alltext = response.css('article p *::text, article p::text').getall()

        # Uso de .get() seguro para evitar erro caso a tag não exista
        time_element = response.css('article time')
        data_da_publicacao = time_element.attrib.get('datetime') if time_element else None
        
        if not data_da_publicacao:
            return

        news = juntar_texto(alltext)

        yield { 
                'Portal': 'R7',
                'titulo': response.css('article h1::text').get(),
                'data_publicacao': transformar_padrao_data(data_da_publicacao),
                'fonte_url': response.url,
                'conteudo': formatar_texto(news)
            }

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def play_wright():
    # Inicia o Playwright
    data = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")
    urls = []
    
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        
        page.goto("https://www.r7.com/tudo-sobre/feminicidio/", wait_until='domcontentloaded')
        
        # Loop para clicar no botão "Veja mais"
        while True:
            try:
                # Localiza todos os itens atuais
                itens = page.locator('[class = b-ultimas-list__items] > li').all()
                
                # Verifica a data no último item visível para decidir se clica
                if itens:
                    pegar_data = itens[-1].locator('time').first.get_attribute("datetime") or ""
                    
                    botao = page.get_by_text("Veja mais Notícias")
                    if botao.is_visible() and data in pegar_data:
                        botao.click()
                        page.wait_for_timeout(5000) # Espera carregar
                    else:
                        break
                else:
                    break
            except Exception:
                break
        
        # Coleta final dos links após expansão
        itens_finais = page.locator('[class = b-ultimas-list__items] > li').all()
        for news in itens_finais:
            pegar_data = news.locator('time').first.get_attribute("datetime") or ""
            pegar_link = news.locator('a').first.get_attribute("href")
            if data in pegar_data and pegar_link:
                urls.append(pegar_link)
        
        browser.close()
    return urls

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def r7_run_spider():
    urls = play_wright() 
    
    if not urls:
        print("Nenhuma URL encontrada para a data de hoje.")
        return

    settings = get_project_settings()
    settings.set(
        'FEEDS',
        {
            'scrapers/resultados/r7.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True
            }
        }
    )
    process = CrawlerProcess(settings)
    process.crawl(r7_spider, urls=urls)
    process.start()