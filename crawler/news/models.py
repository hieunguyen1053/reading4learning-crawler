import logging
from urllib.parse import urlparse

from django.db import models
from django.utils.translation import gettext_lazy as _
from domonic.dom import *
from domonic.html import *
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging

from .apps import scheduler
from .scraper.spiders.news import WebsiteSpider


# Create your models here.
class Website(models.Model):
    class SchedulerType(models.TextChoices):
        ONCE = 'once', _('Once')
        HOURLY = 'hourly', _('Hourly')
        DAILY = 'daily', _('Daily')

    name = models.CharField(max_length=100)
    url = models.URLField(max_length=100, unique=True)

    concurrent_requests = models.IntegerField(default=4)
    download_delay = models.FloatField(default=0.5)
    cookies_enable = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    scheduler_type = models.CharField(
        max_length=32,
        choices=SchedulerType.choices,
        default=SchedulerType.ONCE)

    start_time = models.TimeField()
    start_date = models.DateField()
    job_id = models.CharField(max_length=256)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Website')
        verbose_name_plural = _('Websites')

    def __str__(self):
        return self.name

    @property
    def config(self):
        settings = Settings()
        settings.set('SPIDER_MODULES', ['news.scraper.spiders'])
        settings.set('NEWSPIDER_MODULE', 'news.scraper.spiders')
        settings.set('ROBOTSTXT_OBEY', True)
        settings.set('ITEM_PIPELINES', {
                     'news.scraper.pipelines.WriteDBPipeline': 300})
        settings.set('DUPEFILTER_CLASS',
                     'news.scraper.dupefilters.CustomDupeFilter')
        settings.set('DUPEFILTER_DEBUG', True)
        settings.set('CONCURRENT_REQUESTS', self.concurrent_requests)
        settings.set('DOWNLOAD_DELAY', self.download_delay)
        settings.set('COOKIES_ENABLED', self.cookies_enable)
        return settings

    def start_crawling(self):
        if not self.is_active:
            return

        configure_logging()
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('newspaper').setLevel(logging.WARNING)
        process = CrawlerRunner(self.config)
        process.crawl(WebsiteSpider, name=self.name, url=self.url, domain=urlparse(self.url).netloc)

    def update_job(self):
        if self.job_id is not None:
            try:
                scheduler.remove_job(job_id=self.job_id)
            except:
                pass

        job_id = None
        if self.scheduler_type == 'once':
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger='date',
                run_date='{} {}'.format(self.start_date, self.start_time),
            ).id

        if self.scheduler_type == 'hourly':
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger='cron',
                args=[self],
                minute=self.start_time.minute
            ).id

        if self.scheduler_type == 'daily':
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger='cron',
                minute=self.start_time.minute,
                hour=self.start_time.hour
            ).id

        self.job_id = job_id


class News(models.Model):
    url = models.URLField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    top_image = models.URLField(max_length=100)
    author = models.CharField(max_length=100)
    publish_date = models.DateField()

    categories = models.CharField(max_length=256)

    statistics = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')

    @property
    def html(self):
        result = HTMLDivElement()

        title = HTMLHeadingElement()
        title.nodeValue = self.title
        result.append(title)

        categories = HTMLSpanElement()
        categories.nodeValue = self.categories
        categories.nodeValue = ', '.join([c.title() for c in eval(self.categories)])
        result.append(categories)

        result.append(HTMLBRElement())

        author = HTMLSpanElement()
        authors = eval(self.author)
        if len(authors) > 1:
            author.nodeValue = 'Authors: ' + ' '.join(authors)
        else:
            author.nodeValue = 'Author: ' + authors[0]
        result.append(author)

        result.append(HTMLBRElement())

        publish_date = HTMLSpanElement()
        publish_date.nodeValue = self.publish_date.strftime('%Y %b, %d')
        result.append(publish_date)

        result.append(HTMLBRElement())

        content = self.content.split('\n')
        paragraph = HTMLParagraphElement()
        paragraph.nodeValue = content[0]
        content.pop(0)

        result.append(paragraph)

        image = HTMLImageElement()
        image.setAttribute('src', self.top_image)
        image.setAttribute('style', 'width: 100%;')
        result.append(image)

        for line in content:
            if line.isupper():
                paragraph = HTMLElement()
                paragraph.name = 'h4'
            else:
                paragraph = HTMLParagraphElement()
            paragraph.nodeValue = line
            result.append(paragraph)

        reference = HTMLSpanElement()
        anchor = HTMLAnchorElement()
        anchor.setAttribute('href', self.url)
        anchor.nodeValue = self.url

        reference.append("Source: ")
        reference.append(anchor)
        result.append(reference)

        return result.toString()
