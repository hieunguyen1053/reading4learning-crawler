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


class Vocab(models.Model):
    idf = models.TextField()
    topk = models.IntegerField(default=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vocab'
        verbose_name_plural = 'Vocab'

    def __str__(self):
        return "tedtalks_{}_{}".format(self.topk, self.created_at)

    def get_vocab(self):
        vocab = []
        lines = self.idf.split('\n')
        for line in lines:
            if line == '':
                continue
            word, idf = line.split('\t')
            vocab.append(word)
        return vocab

    def vocab(self):
        return '\n'.join(self.get_vocab())
