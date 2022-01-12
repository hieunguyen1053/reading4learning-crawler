from django.contrib import admin

from .models import Word, WordField, WordTarget, Field, Target


# Register your models here.
@admin.register(Word)
class WordAdmin(admin.ModelAdmin):

    class WordFieldInline(admin.TabularInline):
        model = WordField
        extra = 0
        fields = ('field', 'idf')
        readonly_fields = ('idf',)

    class WordTargetInline(admin.TabularInline):
        model = WordTarget
        extra = 0
        fields = ('target', 'idf')
        readonly_fields = ('idf',)

    list_display = ('word', 'created_at', 'updated_at')
    inlines = (WordFieldInline, WordTargetInline)
    list_filter = ('created_at', 'updated_at')
    search_fields = ('word',)


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
