from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, UpdateView, DetailView
import json
# Create your views here.


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/news.html'
    context_object_name = 'article'


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'news/add.html'
    fields = ['title', 'anouncement', 'text', 'tags']


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = '/news'
    template_name = 'news/delete.html'


@login_required(login_url='login')
def news_add(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()
            return redirect('news_index')
    else:
        form = ArticleForm()
    return render(request, 'news/add.html', {'form': form})


def news_index(request):
    articles = Article.objects.all().order_by('-date')
    # comments = Comment.objects.all()
    # for a in articles:
    #     print(a.title, a.tags.all())
    # articles2 = Article.objects.filter(author=request.user.id)
    # print('Автор новости', article.title, ':', article.author.account.gender)
    context = {'articles': articles,
               # 'comments': comments
               }
    return render(request, 'news/index.html', context)


def news_user(request):
    articles = Article.objects.filter(author=request.user).order_by('-date')
    # comments = Comment.objects.all()
    # for a in articles:
    #     print(a.title, a.tags.all())
    # articles2 = Article.objects.filter(author=request.user.id)
    # print('Автор новости', article.title, ':', article.author.account.gender)
    context = {'articles': articles,
               # 'comments': comments
               }
    return render(request, 'news/index.html', context)


def news_detail(request, id):
    article = Article.objects.get(id=id)
    comments = Comment.objects.filter(article=article).order_by('-date')
    context = {'article': article,
               'comments': comments}
    if request.method == 'POST':
        if request.user.id:
            comment = Comment()
            comment.article = article
            comment.author = request.user
            comment.text = request.POST.get('text')
            comment.save()
            return redirect(article.get_detail_url())
        else:
            return redirect('users_index')
    return render(request, 'news/news.html', context)


def search_auto(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term', '')
        articles = Article.objects.filter(title__icontains=q)
        results = []
        for a in articles:
            results.append(a.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
