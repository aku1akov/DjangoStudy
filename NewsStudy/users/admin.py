from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Count
from .models import *
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'gender',
                    # 'article_count',
                    # 'comment_count',
                    'image_tag']
    list_filter = ['user', 'gender']
    list_per_page = 5

    @admin.display(description='Новостей', ordering='art_count')
    def article_count(self, profile: Profile):
        return profile.art_count

    @admin.display(description='Комментариев', ordering='com_count')
    def comment_count(self, profile: Profile):
        # count = User.objects.annotate()
        return profile.com_count

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     return queryset.annotate(
    #         # art_count=Count('user.article'),
    #         com_count=Count('comment'))
