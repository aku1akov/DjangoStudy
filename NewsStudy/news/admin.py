from django.contrib import admin
from django.db.models.functions import Length
from django.db.models import Count
from .models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-date', 'title', 'author']
    list_display = ['title', 'author', 'date', 'text_length']
    list_filter = ['title', 'author', 'date']
    list_display_links = ['date']
    # list_editable = ['title', 'author']
    # readonly_fields = ['title', 'author']
    prepopulated_fields = {'slug': ['title']}
    list_per_page = 5

    @admin.display(description='Длина текста', ordering='_symbols')
    def text_length(self, article: Article):
        return len(article.text)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(_symbols=Length('text'))


class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'author', 'date']
    list_filter = ['article', 'author', 'date']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'article', 'image_tag']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'tag_count']
    list_filter = ['title', 'status']

    @admin.display(description='Упоминаний', ordering='tag_count')
    def tag_count(self, object):
        return object.tag_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(tag_count=Count('article'))


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(Tag, TagAdmin)
