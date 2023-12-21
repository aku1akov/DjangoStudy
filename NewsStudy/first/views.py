from django.shortcuts import render
from django.db.models import Count
from news.models import Article


def index(request):
    articles = Article.today.all(). \
        select_related('author'). \
        prefetch_related('tags'). \
        order_by('-date'). \
        annotate(Count('comment', distinct=True), Count('tags', distinct=True))
    context = {'articles': articles,
               'title': 'Новости дня'}
    # return render(request, 'first/index.html')
    return render(request, 'news/index.html', context)


def custom_404(request, exception):
    return render(request, 'first/err404.html')
