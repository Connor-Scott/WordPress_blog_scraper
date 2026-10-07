from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.tssspi import TSSspi


def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(TSSspi)
    process.start()


if __name__ == "__main__":
    run_spider()
