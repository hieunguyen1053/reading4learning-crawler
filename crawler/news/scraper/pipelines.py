# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os

from commons.utils import get_word_count
from itemadapter import ItemAdapter

from ..models import News


class WriteDBPipeline:
    def process_item(self, item, spider):
        statistics = get_word_count(item['content'])
        News.objects.update_or_create(
            url=item['url'],
            title=item['title'],
            content=item['content'],
            top_image=item['top_image'],
            author=item['author'],
            publish_date=item['publish_date'],
            categories=item['categories'],
            statistics=statistics,
        )
