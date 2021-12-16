import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ScraperItem


class SubscenceSpider(CrawlSpider):
    name = 'subtitles'
    allowed_domains = ['subscene.com']
    start_urls = ['https://subscene.com/browse/latest/all/1']

    rules = (
        Rule(LinkExtractor(allow=r'/browse/latest/all/\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/subtitles/[a-z0-9\-]+/english/\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/subtitles/english-text/[A-Za-z0-9\-\_]+'), callback='parse_item'),
    )

    def __init__(self, name=None, **kwargs):
        super(SubscenceSpider, self).__init__(name=name, **kwargs)

    def start_requests(self):
        request = scrapy.Request(url=self.start_urls[0])
        request.cookies = {'LanguageFilter': '13'}
        yield request

    def parse_item(self, response):
        item = ScraperItem()
        item['id'] = response.url.split('/')[-1]
        item['url'] = response.url
        referer = response.request.headers[b'Referer'].decode('utf-8')
        item['title'] = referer.split('/')[-3]
        return item
