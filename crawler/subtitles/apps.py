from django.apps import AppConfig
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging

from subtitles.scraper.spiders.subscence import SubscenceSpider

def start_crawling():
    configure_logging()
    settings = Settings()
    settings.set('SPIDER_MODULES', ['subtitles.scraper.spiders'])
    settings.set('ROBOTSTXT_OBEY', True)
    settings.set('SPIDER_MIDDLEWARES', {
        'subtitles.scraper.middlewares.ScraperSpiderMiddleware': 543,
        'subtitles.scraper.middlewares.TooManyRequestsRetryMiddleware': 543,
    })
    settings.set('ITEM_PIPELINES', {'subtitles.scraper.pipelines.WriteDBPipeline': 300})
    settings.set('DUPEFILTER_CLASS', 'subtitles.scraper.dupefilters.CustomDupeFilter')
    settings.set('DUPEFILTER_DEBUG', True)
    settings.set('RETRY_HTTP_CODES', [429])
    settings.set('RETRY_TIMES', 3)
    settings.set('CONCURRENT_REQUESTS', 8)
    settings.set('DOWNLOAD_DELAY', 1.0)
    settings.set('LOG_FILE', 'scraper.subtitles.log')
    process = CrawlerRunner(settings)
    process.crawl(SubscenceSpider)

class SubtitlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subtitles'

    def ready(self):
        pass
        # start_crawling()
