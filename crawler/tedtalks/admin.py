from django.contrib import admin

from .models import TedTalks, Vocab


# Register your models here.
@admin.register(TedTalks)
class TedTalksAdmin(admin.ModelAdmin):
    list_display = ('slug', 'url')
    fields = ('slug', 'url', 'transcript', 'statistics')
    readonly_fields = ('slug', 'url', 'transcript', 'statistics')
    list_per_page = 20

@admin.register(Vocab)
class VocabAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fields = ('idf', 'topk', 'vocab')
    readonly_fields = ('vocab',)
