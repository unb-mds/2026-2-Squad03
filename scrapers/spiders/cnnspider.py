import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime
from zoneinfo import ZoneInfo
from backend.tratamentoDeDados.tratamentoDeTexto import transformar_padrao_data, formatar_texto, juntar_texto

class cnn_spider(scrapy.Spider):
    name = "cnn"

    data = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")
    start_urls = [
        "https://www.cnnbrasil.com.br/tudo-sobre/feminicidio/"
    ]

    def parse(self, response):
        conteudo = response.css("ul figure")
        for pegar_conteudo in conteudo:
            coletar_data = pegar_conteudo.css("time::attr(datetime)").get()

            link = pegar_conteudo.css("a::attr(href)").get()

            if not coletar_data or not link:
                return

            padronizar_data = coletar_data[:10]

            if padronizar_data == self.data:
                yield response.follow(link, callback=self.parse_ir)
            else:
                continue

    def parse_ir(self, response, **kwargs):
        alltext = response.css('article p *::text, article p::text, article p strong::text').getall()
        # 2026-01-10
        
        data_da_publicacao = response.css('article time').attrib['datetime']

            # colocanto toda a noticia em uma unica string
        news = juntar_texto(alltext)
        
        yield {
                'Portal': 'CNN',
                'titulo': response.css('article').css('header').css('h1::text').get(),
                'data_publicacao': transformar_padrao_data(data_da_publicacao),
                'fonte_url': response.url,
                'conteudo':  formatar_texto(news)
        }

         
def cnn_run_spider():
    settings = get_project_settings()
    settings.set(
        'FEEDS',
        {
            'scrapers/resultados/cnn.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True
            }
        }
    )
    process = CrawlerProcess(settings)
    process.crawl(cnn_spider)
    process.start()
