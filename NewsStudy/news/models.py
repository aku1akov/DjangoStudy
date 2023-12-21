from django.db import models
from django.contrib.auth.models import User
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

    class Meta:
        ordering = ['title', 'status']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Article(models.Model):
    categories = (('Ec', 'Economy'),
                  ('Sc', 'Science'),
                  ('IT', 'IT'))

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    title = models.CharField('Название', max_length=50, default='')
    anouncement = models.TextField('Аннотация', max_length=250)
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата создания', auto_now=True)
    category = models.CharField(choices=categories, max_length=20, verbose_name='Категории')
    tags = models.ManyToManyField(verbose_name='Тэги', to=Tag, blank=True)

    objects = models.Manager()
    today = Today()

    def __str__(self):
        return f'{self.title} от {self.date}'

    def get_absolute_url(self):
        return f'/news/detail/{self.pk}'

    def get_update_url(self):
        return f'/news/update/{self.pk}'

    def get_delete_url(self):
        return f'/news/delete/{self.pk}'

    def tag_list(self):
        s = ''
        for t in self.tags:
            s += t.title + ' '
        return s

    class Meta:
        ordering = ['title', 'date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False)
    text = models.TextField('Текст комментария')
    date = models.DateTimeField('Время создания', auto_now_add=True)

    def __str__(self):
        return f'Комменарий от: {self.date}'

    class Meta:
        ordering = ['article', 'date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

