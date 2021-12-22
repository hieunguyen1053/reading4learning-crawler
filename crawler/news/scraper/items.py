# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    url = scrapy.Field()

    title = scrapy.Field()
    content = scrapy.Field()
    top_image = scrapy.Field()
    author = scrapy.Field()
    publish_date = scrapy.Field()

    categories = scrapy.Field()
    statistics = scrapy.Field()