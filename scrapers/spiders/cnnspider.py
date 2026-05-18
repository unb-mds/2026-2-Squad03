import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime

class cnn_spider(scrapy.Spider):
    name = 'CNN'
    data = str(datetime.now().strftime("%Y-%m-%d"))
    links = []
    i = 1

    def start_requests(self):
        yield scrapy.Request('https://www.cnnbrasil.com.br/tudo-sobre/feminicidio/')

    def parse(self, response, **kwargs):
        for news in response.css('ul figure'):
            if (self.data in news.css('time').attrib['datetime']):
                yield response.follow(news.css('a').attrib['href'], self.parse_pegar)

        pag = response.css('a:contains("Pr")::attr(href)').get() 

        if pag:
            yield response.follow(pag, self.parse)
        else:
            yield response.follow(self.links[0], self.parse_pegar)

    def parse_pegar(self, response):
        alltext = response.css('.text-lg p::text').getall()
        news = ''
        for text in alltext:
             news+= text

        yield {
                'portal': 'CNN',
                'title': response.css('article').css('header').css('h1::text').get(),
                'data': response.css('article').css('span').css('.timestamp__date::text').getall(),
                'links': response.css('ul figure a').attrib['href'],
                'texto':  news,
                'autor': response.css('article').css('header').css('span').css('a').css('span::text').get()
        }
        for self.i in range(len(self.links)):
                get = self.links[self.i]
                self.i += 1
                yield response.follow(get, self.parse_pegar)

              
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
