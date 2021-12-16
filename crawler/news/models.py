from django.core.exceptions import ValidationError
from django.db import models

from .regex_generator.generator import generator


# Create your models here.
class News(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)

    example_categories = models.TextField(blank=True)
    example_items = models.TextField(blank=True)

    category_regex = models.CharField(max_length=100, blank=True)
    item_regex = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.example_categories and not self.category_regex:
            raise ValidationError('Must specify either example categories or regex')
        if not self.example_items and not self.item_regex:
            raise ValidationError('Must specify either example items or regex')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def generate_category_regex(self):
        if self.example_categories and not self.category_regex:
            target = self.example_categories.split('\n')
            target = [x.strip() for x in target]
            result = generator(target, 100, 10)
            result = sorted(result, key=lambda x: -x[0])
            regex = result[0][1]
            self.category_regex = regex
            self.save()

    def generate_item_regex(self):
        if self.example_items and not self.item_regex:
            target = self.example_items.split('\n')
            target = [x.strip() for x in target]
            result = generator(target, 100, 10)
            result = sorted(result, key=lambda x: -x[0])
            regex = result[0][1]
            self.item_regex = regex
            self.save()
