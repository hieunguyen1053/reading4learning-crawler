from django.test import TestCase

# Create your tests here.
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging

from scraper.spiders.subscence import SubscenceSpider

configure_logging()
settings = Settings()
settings.setmodule('scraper.settings')
process = CrawlerProcess(settings)
process.crawl(SubscenceSpider)
process.start()