from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, UpdateView, DetailView
from django.db.models import Count
import json


# Create your views here.


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/news.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cur_obj = self.object
        comments = Comment.objects.filter(article=cur_obj).order_by('-date')
        images = Image.objects.filter(article=cur_obj)
        context['images'] = images
        context['comments'] = comments
        return context


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'news/add.html'
    fields = ['title', 'anouncement', 'text', 'tags']


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('news_index')
    template_name = 'news/delete.html'


@login_required(login_url='login')
def news_add(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()
            for image in request.FILES.getlist('image_field'):
                Image.objects.create(article=article, image=image, title=image.name)
            return redirect('news_index')
    else:
        form = ArticleForm()
    return render(request, 'news/add.html', {'form': form})


def news_index(request):
    articles = Article.objects.\
        select_related('author').\
        prefetch_related('tags').\
        order_by('-date').\
        annotate(Count('comment', distinct=True), Count('tags', distinct=True)).all()
    context = {'articles': articles,
               'title': 'Все новости'}
    return render(request, 'news/index.html', context)


def news_user(request):
    articles = Article.objects.filter(author=request.user).\
        select_related('author').\
        prefetch_related('tags').\
        order_by('-date').\
        annotate(Count('comment', distinct=True), Count('tags', distinct=True))
    context = {'articles': articles,
               'title': 'Мои новости'}
    return render(request, 'news/index.html', context)


def news_detail(request, id):
    article = Article.objects.select_related('author').get(id=id)
    comments = Comment.objects.select_related('author').filter(article=article).order_by('-date')
    images = Image.objects.filter(article=article)
    context = {'article': article,
               'comments': comments,
               'images': images}
    if request.method == 'POST':
        if request.user.id:
            comment = Comment()
            comment.article = article
            comment.author = request.user
            comment.text = request.POST.get('text')
            comment.save()
            return redirect('news_detail', id)
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
