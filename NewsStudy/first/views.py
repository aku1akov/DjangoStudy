from django.shortcuts import render
from django.db.models import Count
from news.models import Article


def index(request):
    # print('!!!!')
    # articles = Article.today.all(). \
    #     select_related('author'). \
    #     prefetch_related('tags'). \
    #     order_by('-date'). \
    #     annotate(Count('comments', distinct=True))
    # context = {'articles': articles,
    #            'title': 'Новости дня'}
    # return render(request, 'first/index.html')
    return render(request, 'first/index.html', {'title': 'Главная страница'})


def custom_404(request, exception):
    return render(request, 'first/err404.html')
