import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

DIR = os.path.dirname(os.path.abspath(__file__))
my_dict = open(os.path.join(DIR, 'references/words_alpha.txt'), 'r').read().split('\n')

class Word(models.Model):
    word = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('word',)
        verbose_name = _('Word')
        verbose_name_plural = _('Words')

    def clean(self):
        if self.word not in my_dict:
            raise ValidationError(_('%(value)s is not in the dictionary'), params={'value': self.word})

    def __str__(self):
        return self.word


class Field(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')

    def __str__(self):
        return self.name


class WordField(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    idf = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('word', 'field')

class Target(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Target')
        verbose_name_plural = _('Targets')

    def __str__(self):
        return self.name


class WordTarget(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    idf = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('word', 'target')
