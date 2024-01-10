from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models import Count
from datetime import date
# Create your models here.


class Today(models.Manager):
    def get_queryset(self):
        return super(Today, self).get_queryset().filter(date__gte=date.today())


class Tag(models.Model):
    title = models.CharField(max_length=80)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @admin.display(description='Количество новостей')
    def tag_count(self):
        return Article.objects.filter(tags=self).count()

    class Meta:
        ordering = ['title', 'status']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Article(models.Model):
    categories = (('Ec', 'Economy'),
                  ('Sc', 'Science'),
                  ('IT', 'IT'))

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    title = models.CharField('Заголовок', max_length=50, default='')
    anouncement = models.TextField('Аннотация', max_length=250)
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата создания', auto_now=True)
    # category = models.CharField(choices=categories, max_length=20, verbose_name='Категория')
    tags = models.ManyToManyField(verbose_name='Тэги', to=Tag, blank=True)
    slug = models.SlugField()

    objects = models.Manager()
    today = Today()

    def __str__(self):
        return f'{self.title} от {self.date}'

    def get_absolute_url(self):
        return f'/news/detail/{self.pk}'

    # def get_update_url(self):
    #     return f'/news/update/{self.pk}'
    #
    # def get_delete_url(self):
    #     return f'/news/delete/{self.pk}'

    def tag_list(self):
        s = ''
        for t in self.tags.all():
            s += t.title + ' '
        return s

    @admin.display(description='Изображение')
    def image_tag(self):
        image = Image.objects.filter(article=self).first()
        if image:
            return mark_safe(f'<img src="{image.image.url}" height="50px" width="auto"/>')
        else:
            return f'no image'

    @admin.display(description='Просмотров')
    def views_count(self):
        return self.views.count()

    @admin.display(description='Комментариев')
    def comments_count(self):
        return self.comments.count()

    @admin.display(description='Изображений')
    def images_count(self):
        return self.images.count()

    class Meta:
        ordering = ['title', 'date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False, related_name='comments')
    text = models.TextField('Текст комментария')
    date = models.DateTimeField('Время создания', auto_now_add=True)

    def __str__(self):
        return f'Комменарий от: {self.date}'

    class Meta:
        ordering = ['article', 'date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=50, blank=True, verbose_name='Название')
    image = models.ImageField(upload_to='news_img', verbose_name='Изображение')

    def __str__(self):
        return self.title

    @admin.display(description='Изображение')
    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" height="50px" width="auto"/>')

    class Meta:
        ordering = ['article', 'title']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class ViewCount(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='views', verbose_name='Новость')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    ip = models.GenericIPAddressField(verbose_name='IP адрес')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.article.title

    class Meta:
        ordering = ['-date']
        indexes = [models.Index(fields=['-date'])]
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'