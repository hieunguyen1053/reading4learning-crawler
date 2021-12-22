# Create your tests here.
import logging

from django.test import TestCase
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging

from scraper.spiders.news import WebsiteSpider

configure_logging()

logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('protego').setLevel(logging.WARNING)
logging.getLogger('newspaper').setLevel(logging.WARNING)

settings = Settings()
settings.setmodule('scraper.settings')
process = CrawlerProcess(settings)
process.crawl(WebsiteSpider)
process.start()
