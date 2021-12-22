import scrapy
from newspaper import Source

from ..items import ScraperItem
from ..mynewspaper import MyArticle as Article


class WebsiteSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name')
        url = kwargs.get('url')
        domain = kwargs.get('domain')

        self.allowed_domains = [domain]
        self.start_urls = [url]
        super(WebsiteSpider, self).__init__(name=name, **kwargs)

    @property
    def header(self):
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

    def start_requests(self):
        root = Source(self.start_urls[0], memoize_articles=False)
        root.download()
        root.parse()
        root.set_categories()
        root.download_categories()
        root.parse_categories()

        for category in root.category_urls():
            yield scrapy.Request(url=category, callback=self.parse, headers=self.header)

    def parse(self, response):
        root = Source(response.url, memoize_articles=False)
        root.html = response.body
        root.parse()
        root.set_categories()
        root.download_categories()
        root.parse_categories()
        root.generate_articles()

        for article in root.article_urls():
            yield scrapy.Request(url=article, callback=self.parse_item, headers=self.header)

    def parse_item(self, response):
        article = Article(response.url, keep_article_html=True)
        article.set_html(response.body)
        article.parse()

        if not article.is_valid_body():
            return

        item = ScraperItem()
        item['url'] = response.url
        item['title'] = article.title
        item['content'] = article.text
        item['top_image'] = article.top_image
        item['author'] = article.authors
        item['publish_date'] = article.publish_date
        item['categories'] = article.categories

        return item
