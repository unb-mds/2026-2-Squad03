from multiprocessing import Process
from spiders.g1Spider import g1_run_spider
from spiders.cnnspider import cnn_run_spider
from spiders.r7spider import r7_run_spider
from spiders.metropoles import metropoles_run_spider
from salvarscrapys import salvar_todos_resultados

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def main():
    g1_scrapy = Process(target = g1_run_spider)
    g1_scrapy.start()
    g1_scrapy.join()

    cnn_scrapy = Process(target= cnn_run_spider)
    cnn_scrapy.start()
    cnn_scrapy.join()

    r7_scrapy = Process(target= r7_run_spider)
    r7_scrapy.start()
    r7_scrapy.join()

    metropoles_scrapy = Process(target= metropoles_run_spider)
    metropoles_scrapy.start()
    metropoles_scrapy.join()
    salvar_todos_resultados()

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

if __name__ == "__main__":
    main()
    
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+