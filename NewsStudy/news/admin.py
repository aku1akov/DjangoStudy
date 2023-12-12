from django.contrib import admin
from .models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date']
    list_filter = ['title', 'author', 'date']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'author', 'date']
    list_filter = ['article', 'author', 'date']


class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['title', 'status']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
