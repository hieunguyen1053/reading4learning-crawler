from django.db import models


# Create your models here.
class TedTalks(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    url = models.URLField(max_length=200, unique=True)
    transcript = models.TextField()
    statistics = models.TextField()

    class Meta:
        verbose_name = 'Ted Talks'
        verbose_name_plural = 'Ted Talks'

    def __str__(self):
        return self.slug
