from django.contrib import admin

from .models import Subtitles

# Register your models here.


@admin.register(Subtitles)
class SubtitlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'referer')
    fields = ('title', 'referer', 'transcript', 'statistics')
    readonly_fields = ('title', 'referer', 'transcript', 'statistics')
    list_per_page = 20
