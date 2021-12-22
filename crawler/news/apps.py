from apscheduler.schedulers.background import BackgroundScheduler
from crochet import setup
from django.apps import AppConfig

setup()
scheduler = BackgroundScheduler()

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.start()

        from . import signals
