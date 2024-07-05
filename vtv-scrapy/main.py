import logging
import os
from logging.handlers import RotatingFileHandler
from scrapy.utils.log import configure_logging

from vtvscraper.spiders.vtvspider import VtvSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename="log.txt",
    #     format='%(levelname)s: %(message)s',
    #     level=logging.INFO,
    #     filemode='a'
    # )
    os.environ['SCRAPY_MODE'] = "prod"
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    my_handler = RotatingFileHandler(
        filename='vtv-crawler.log',
        mode='a',
        maxBytes=10 * 1024 * 1024,
        backupCount=2,
        encoding='utf-8'
    )
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.INFO)
    app_log.addHandler(my_handler)
    process = CrawlerProcess(get_project_settings())
    process.crawl(VtvSpider)
    process.start()


if __name__ == '__main__':
    main()
