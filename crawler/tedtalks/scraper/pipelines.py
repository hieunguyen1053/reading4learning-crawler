# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from ..models import TedTalks
from ..utils import get_word_count

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, '../data')

class WriteFilePipeline:
    def process_item(self, item, spider):
        with open(os.path.join(DATA, item['slug'] + '.txt'), 'w') as f:
            f.write(item['transcript'])
        return item

class WriteDBPipeline:
    def process_item(self, item, spider):
        statistics = get_word_count(item['transcript'])

        TedTalks.objects.update_or_create(
            slug=item['slug'],
            url=item['url'],
            transcript=item['transcript'],
            statistics=statistics,
        )
        return item
