import sys
import os
import platform
from datetime import datetime

# Adiciona a pasta raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

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

class cnn_spider(scrapy.Spider):
    name = "cnn"
    start_urls = ["https://www.cnnbrasil.com.br/tudo-sobre/feminicidio/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Calcula a data atual apenas no momento da execução
        self.data = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

    def parse(self, response):
        conteudo = response.css("ul figure")
        for pegar_conteudo in conteudo:
            coletar_data = pegar_conteudo.css("time::attr(datetime)").get()
            link = pegar_conteudo.css("a::attr(href)").get()

            if not coletar_data or not link:
                continue

            # A data na CNN pode vir com formato ISO completo, pegamos apenas a parte da data
            padronizar_data = coletar_data[:10]

            if padronizar_data == self.data:
                yield response.follow(link, callback=self.parse_ir)

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

    def parse_ir(self, response, **kwargs):
        alltext = response.css('article p *::text, article p::text, article p strong::text').getall()
        
        # Uso de .get() com fallback para evitar que o spider pare se o campo não existir
        time_element = response.css('article time')
        data_da_publicacao = time_element.attrib.get('datetime') if time_element else None
        
        if not data_da_publicacao:
            return

        news = juntar_texto(alltext)
        
        yield {
                'Portal': 'CNN',
                'titulo': response.css('article header h1::text').get(),
                'data_publicacao': transformar_padrao_data(data_da_publicacao),
                'fonte_url': response.url,
                'conteudo': formatar_texto(news)
        }

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def cnn_run_spider():
    settings = get_project_settings()
    settings.set('FEEDS', {
        'scrapers/resultados/cnn.json': {
            'format': 'json',
            'encoding': 'utf-8',
            'overwrite': True
        }
    })
    process = CrawlerProcess(settings)
    process.crawl(cnn_spider)
    process.start()