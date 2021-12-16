# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    url = scrapy.Field()
    slug = scrapy.Field()
    transcript = scrapy.Field()
