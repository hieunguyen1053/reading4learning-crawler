# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import io
import os
import re
import zipfile

import requests
from bs4 import BeautifulSoup
from itemadapter import ItemAdapter

from ..models import Subtitles
from ..utils import get_word_count

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, '../data')


class WriteDBPipeline:
    def process_item(self, item, spider):
        zip_file = self.download_file(item)
        data = self.extract_srt_file(zip_file)
        content = self.extract_text(data)

        transcript = '\n'.join(content)
        statistics = get_word_count(transcript)

        Subtitles.objects.update_or_create(
            title=item['title'],
            url=item['url'],
            referer=item['referer'],
            transcript='\n'.join(content),
            statistics=statistics,
        )
        return item

    def download_file(self, item):
        resp = requests.get(item['url'])
        zip_file = resp.content
        zip_file = zipfile.ZipFile(io.BytesIO(zip_file))
        return zip_file

    def extract_srt_file(self, zip_file):
        data = zip_file.read(zip_file.namelist()[0])
        return data.decode('utf-8')

    def extract_text(self, data):
        data = re.sub('\r\n', '\n', data)
        data = re.sub('<i>', '', data)
        data = re.sub('</i>', '', data)
        data = re.findall('(?P<index>\d+)\n(?P<time>[\d\:\,\-\>\s]+)\n(?P<content>.+)', data)
        data = map(lambda x: x[-1], data)
        data = map(lambda x: BeautifulSoup(x, 'html.parser').get_text(), data)
        return list(data)
