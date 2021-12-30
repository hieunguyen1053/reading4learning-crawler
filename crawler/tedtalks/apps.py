from django.apps import AppConfig
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging

from tedtalks.scraper.spiders.tedtalks import TedSpider


def start_crawling():
    configure_logging()
    settings = Settings()
    settings.set('SPIDER_MODULES', ['tedtalks.scraper.spiders'])
    settings.set('ROBOTSTXT_OBEY', True)
    settings.set('SPIDER_MIDDLEWARES', {
        'tedtalks.scraper.middlewares.ScraperSpiderMiddleware': 543,
        'tedtalks.scraper.middlewares.TooManyRequestsRetryMiddleware': 543,
    })
    settings.set('ITEM_PIPELINES', {'tedtalks.scraper.pipelines.WriteDBPipeline': 300})
    settings.set('DUPEFILTER_CLASS', 'tedtalks.scraper.dupefilters.CustomDupeFilter')
    settings.set('DUPEFILTER_DEBUG', True)
    settings.set('RETRY_HTTP_CODES', [429])
    settings.set('RETRY_TIMES', 3)
    settings.set('CONCURRENT_REQUESTS', 8)
    settings.set('DOWNLOAD_DELAY', 0.5)
    settings.set('LOG_FILE', 'scraper.tedtalks.log')
    process = CrawlerRunner(settings)
    process.crawl(TedSpider)

class TedtalksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tedtalks'

    def ready(self):
        pass
        # start_crawling()
