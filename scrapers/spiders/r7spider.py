import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from playwright.sync_api import sync_playwright
import time
from datetime import datetime

class r7_spider(scrapy.Spider):
    name = 'r7'

    def __init__(self, urls = None, **kwargs):
        self.start_urls = urls or []

    def parse(self, response, **kwargs):
        alltext = response.css('article p *::text, article p::text').getall()

        # colocanto toda a noticia em uma unica string

        news = ' '.join(
            t.strip()
            for t in alltext
            if t.strip() )


        yield { 
                'portal': 'R7',
                'title': response.css('article h1::text').get(),
                'data': response.css('article time::text').get(),
                'link': response.url,
                'news': news
            }


def play_wright():
    # Inicia o Playwright
    data = str(datetime.now().strftime("%Y-%m-%d"))
    urls = []
    with sync_playwright() as p:

        browser = p.firefox.launch(headless=True)


        page = browser.new_page()
        page.goto("https://www.r7.com/tudo-sobre/feminicidio/", wait_until='domcontentloaded')
        teste = page.locator('[class = b-ultimas-list__items] > li').all()  
        
        while True:
            for dates_in in teste:
                    pegar_data = dates_in.locator('time').first.get_attribute(name="datetime")
                    ultima = pegar_data
            try:
                # Tenta localizar o botão "ver mais"
                botao = page.get_by_text("Veja mais Notícias")
                
                if botao.is_visible() and data in ultima:
                    botao.click()
                    page.wait_for_timeout(10000)  # espera carregar
                else: break
            except Exception:
                # Se não encontrar mais o botão, sai do loop
                break

        
        for test in teste:
            pegar_data = test.locator('time').first.get_attribute(name="datetime")
            pegar_link = test.locator('a').first.get_attribute(name="href")
            if data in pegar_data:
                urls.append(pegar_link)
        
        # print(urls)
        browser.close()
    return urls

def r7_run_spider():
    
    # pegando os urls com o playwritght

    urls = play_wright() 

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
    process.crawl(r7_spider, urls)
    process.start()
