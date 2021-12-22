from gettext import ngettext

from django.contrib import admin, messages
from django.db.models import fields

from .apps import scheduler
# Register your models here.
from .models import Website, News


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    actions = ('setup_crawler', 'stop_crawler')
    list_display = ('name', 'scheduler_type', 'start_time',
                    'start_date', 'is_active')
    search_fields = ('name', 'url')
    readonly_fields = ('created_at', 'updated_at', 'job_id')
    fieldsets = (
        (None, {
            'fields': ('name', 'url', 'created_at', 'updated_at', 'job_id')
        }),
        ('Config', {
            'fields': ('concurrent_requests', 'download_delay', 'cookies_enable')
        }),
        ('Scheduler', {
            'fields': ('scheduler_type', 'start_time', 'start_date', 'is_active')
        })
    )

    @admin.action(description='Start crawling now')
    def setup_crawler(self, request, queryset):
        for query in queryset:
            query.start_crawling()

        self.message_user(request, ngettext(
            '%d scraper was successfully running.',
            '%d scrapers were successfully running.',
            len(queryset),
        ) % len(queryset), messages.SUCCESS)

    @admin.action(description='Disable crawler')
    def stop_crawler(self, request, queryset):
        for query in queryset:
            scheduler.remove_job(query.job_id)
        self.message_user(request, ngettext(
            '%d scraper was successfully disabled.',
            '%d scrapers were successfully disbled.',
            len(queryset),
        ) % len(queryset), messages.SUCCESS)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ('title', 'url')
    readonly_fields = ('html',)

    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'top_image', 'author', 'publish_date', 'categories')}),
        ('HTML', {'fields': ('html',)}),
        ('Statistics', {'fields': ('statistics',)}),
    )