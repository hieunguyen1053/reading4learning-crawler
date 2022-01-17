import logging
import uuid
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

    name = models.CharField(max_length=256)
    url = models.URLField(max_length=256, unique=True)

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
        process.crawl(WebsiteSpider, name=self.name, url=self.url,
                      domain=urlparse(self.url).netloc)

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


class Category(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['parent__name', 'name']

    def get_childs(self):
        return Category.objects.filter(parent=self)

    def __str__(self):
        if self.parent:
            return '{} - {}'.format(self.parent.name, self.name)
        return self.name


class News(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    html_content = models.TextField()
    content = models.TextField()

    author = models.CharField(max_length=256, blank=True, null=True)
    date_published = models.DateField()

    lead_image_url = models.URLField(max_length=256)
    url = models.URLField(max_length=256, unique=True)
    domain = models.CharField(max_length=256)

    word_count = models.IntegerField()
    statistics = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    categories = models.ManyToManyField(Category, blank=True)

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
