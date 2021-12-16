from django.contrib import admin

# Register your models here.
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'created_at', 'updated_at')
    search_fields = ('name', 'domain')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'domain', 'created_at', 'updated_at')
        }),
        ('Category', {
            'fields': ('example_categories', 'category_regex',)
        }),
        ('Item', {
            'fields': ('example_items', 'item_regex',)
        })
    )