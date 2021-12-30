from django.db import models


# Create your models here.
class Subtitles(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200, unique=True)
    referer = models.URLField(max_length=200, unique=True)
    transcript = models.TextField()
    statistics = models.TextField()

    class Meta:
        verbose_name = 'Subtitle'
        verbose_name_plural = 'Subtitles'

    def __str__(self):
        return self.title
