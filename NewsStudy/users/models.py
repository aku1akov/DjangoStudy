from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from news.models import Article, Comment


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, verbose_name='Пользователь')
    nickname = models.CharField(verbose_name='Никнейм', max_length=100)
    birthdate = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    website = models.URLField(verbose_name='Персональный сайт', blank=True)
    github = models.URLField(verbose_name='Github', blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=20, blank=True)
    image = models.ImageField(verbose_name='Иконка', default='default_profile.jpg',
                              upload_to='profile_img')

    def __str__(self):
        return f"{self.user.username} profile"

    @admin.display(description='Иконка профиля')
    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" height="50px" width="auto"/>')

    def art_count(self):
        return Article.objects.filter(author=self.user).count()

    def com_count(self):
        return Comment.objects.filter(author=self.user).count()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили пользователей'


class FavoriteArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='favorites')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Новость', related_name='favorites')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        ordering = ['date', 'user']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
