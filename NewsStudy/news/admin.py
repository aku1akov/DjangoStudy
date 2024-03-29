from django.contrib import admin
from django.db.models.functions import Length
from django.db.models import Count
from .models import *
# Register your models here.


class ArticleCategoryFilter(admin.SimpleListFilter):
    title = 'По категориям'
    parameter_name = 'top'

    def lookups(self, request, model_admin):
        return [('V', 'Топ по просмотрам, >5'),
                ('C', 'Топ по комментариям, >5'),
                ('F', 'Топ избранного, >5 раз')]

    def queryset(self, request, queryset):
        if self.value() == 'V':
            return queryset.annotate(v_count=Count('views')).filter(v_count__gte=6).order_by('-v_count', '-date')
        elif self.value() == 'C':
            return queryset.annotate(c_count=Count('comments')).filter(c_count__gte=6).order_by('-c_count', '-date')
        elif self.value() == 'F':
            return queryset.annotate(f_count=Count('favorites')).filter(f_count__gte=6).order_by('-f_count', '-date')


class ArticleLengthFilter(admin.SimpleListFilter):
    title = 'По длине новости'
    parameter_name = 'text'

    def lookups(self, request, model_admin):
        return [('S', 'Короткие, <100 зн.'),
                ('M', 'Средние, 100-500 зн.'),
                ('L', 'Длинные, >500 зн.'),]

    def queryset(self, request, queryset):
        if self.value() == 'S':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=100)
        elif self.value() == 'M':
            return queryset.annotate(text_len=Length('text')).filter(text_len__gte=100,
                                                                     text_len__lte=500)
        elif self.value() == 'L':
            return queryset.annotate(text_len=Length('text')).filter(text_len__gt=500)


class ArticleImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ['id', 'image_tag']


class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-date', 'title', 'author']
    list_display = ['title', 'author', 'date',
                    'text_length',
                    'views_count',
                    'comments_count',
                    # 'images_count',
                    'image_tag']
    list_filter = [ArticleLengthFilter, ArticleCategoryFilter]
    search_fields = ['title', 'tags__title']
    # list_display_links = ['date']
    # list_editable = ['author']
    readonly_fields = ['author']
    prepopulated_fields = {'slug': ['title']}
    list_per_page = 5
    inlines = [ArticleImageInline]
    filter_horizontal = ['tags']

    @admin.display(description='Длина текста', ordering='symbols_count')
    def text_length(self, article: Article):
        return len(article.text)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(symbols_count=Length('text'))


class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'author', 'date']
    list_filter = ['author', 'date']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'article', 'image_tag']


@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'ip', 'date']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'tag_count']
    list_filter = ['title', 'status']
    actions = ['set_true']

    # @admin.display(description='Количество новостей', ordering='tag_count')
    # def tag_count(self, object):
    #     return object.tag_count
    #
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     return queryset.annotate(tag_count=Count('article'))

    @admin.action(description='Активировать выбранные теги')
    def set_true(self, request, queryset):
        amount = queryset.update(status=True)
        self.message_user(request, f'Активировано {amount} тегов')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(Tag, TagAdmin)
