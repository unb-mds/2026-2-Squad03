from multiprocessing import Process
from spiders.g1Spider import g1_run_spider

g1_scrapy = Process(target = g1_run_spider)
g1_scrapy.start()
g1_scrapy.join()