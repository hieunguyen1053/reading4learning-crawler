from django.contrib import admin

from .models import TedTalks


# Register your models here.
@admin.register(TedTalks)
class TedTalksAdmin(admin.ModelAdmin):
    list_display = ('slug', 'url')
    fields = ('slug', 'url', 'transcript', 'statistics')
    readonly_fields = ('slug', 'url', 'transcript', 'statistics')
    list_per_page = 20

    # Hide add button
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
