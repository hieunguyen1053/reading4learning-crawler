from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ScraperItem


class TedSpider(CrawlSpider):
    name = 'ted'
    allowed_domains = ['ted.com']
    start_urls = ['https://www.ted.com/talks?sort=newest']

    rules = (
        Rule(LinkExtractor(allow=r'/talks\?page=\d+&sort=newest'), follow=True),
        Rule(LinkExtractor(allow=r'/talks/[a-z0-9\-]+'), callback='parse_item', process_links='process_links'),
    )

    def __init__(self, *args, **kwargs):
        super(TedSpider, self).__init__(*args, **kwargs)
        self.selectors = {}
        self.selectors['transcript'] = '.Grid__cell > p::text'

    def process_links(self, links):
        for link in links:
            link.url += '/transcript'
            yield link

    def parse_item(self, response):
        item = ScraperItem()
        item['url'] = response.request.url
        item['slug'] = response.request.url.split('/')[-2]
        item['transcript'] = ''
        for transcript in response.css(self.selectors['transcript']).getall():
            item['transcript'] += ' '.join(transcript.split()) + '\n'
        return item
