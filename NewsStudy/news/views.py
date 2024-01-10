from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .models import *
from users.models import FavoriteArticle
from .forms import *
from .utils import ViewCountMixin, get_ip
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, UpdateView, DetailView
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import json


# Create your views here.


class ArticleDetailView(ViewCountMixin, DetailView):
    model = Article
    template_name = 'news/news.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cur_obj = self.object
        context['images'] = Image.objects.filter(article=cur_obj)
        context['comments'] = Comment.objects.filter(article=cur_obj).order_by('-date')
        return context


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'news/add.html'
    fields = ['title', 'anouncement', 'text', 'tags']

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        cur_obj = self.object
        context['image_form'] = ImagesFormSet(instance=cur_obj)
        return context

    def post(self, request, **kwargs):
        print(request.POST)
        cur_obj = Article.objects.get(id=request.POST['images-0-article'])
        del_ids = []
        for i in range(int(request.POST['images-TOTAL_FORMS'])):
            field_delete = f'images-{i}-DELETE'
            field_img_id = f'images-{i}-id'
            if field_delete in request.POST and request.POST[field_delete] == 'on':
                image = Image.objects.get(id=request.POST[field_img_id])
                image.delete()
                del_ids.append(field_img_id)

        for i in range(int(request.POST['images-TOTAL_FORMS'])):
            field_replace = f'images-{i}-image'
            field_img_id = f'images-{i}-id'
            if field_replace in request.FILES and request.POST[field_img_id] != '' and field_img_id not in del_ids:
                image = Image.objects.get(id=request.POST[field_img_id])
                image.delete()
                for img in request.FILES.getlist(field_replace):
                    Image.objects.create(article=cur_obj, image=img, title=img.name)
                del request.FILES[field_replace]
        if request.FILES:
            for input_name in request.FILES:
                for img in request.FILES.getlist(input_name):
                    Image.objects.create(article=cur_obj, image=img, title=img.name)

        return super(ArticleUpdateView, self).post(request, **kwargs)


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


def news_index(request, text=None, id=None):
    if request.session.get('search') and request.build_absolute_uri().endswith('news/'):
        del request.session['search']
    title = 'Все новости'
    articles = Article.objects. \
        select_related('author'). \
        prefetch_related('tags'). \
        order_by('-date'). \
        annotate(Count('comments', distinct=True)).all()

    if request.method == 'POST':
        q = request.POST.get('search')
        articles = articles.filter(
            Q(title__icontains=q) | Q(author__username__icontains=q) | Q(tags__title__icontains=q)).distinct()
        title = f'По запросу найдено новостей: {articles.count()}'
        request.session['search'] = q
    elif request.session.get('search'):
        q = request.session.get('search')
        articles = articles.filter(
            Q(title__icontains=q) | Q(author__username__icontains=q) | Q(tags__title__icontains=q)).distinct()
        title = f'По запросу найдено новостей: {articles.count()}'

    if text == 'author':
        articles = articles.filter(author=id)
        title = f'По запросу найдено новостей: {articles.count()}'
    elif text == 'tags':
        articles = articles.filter(tags=id)
        title = f'По запросу найдено новостей: {articles.count()}'
    elif text == 'bookmark':
        id_list = []
        for el in FavoriteArticle.objects.filter(user_id=id):
            id_list.append(el.article_id)
        articles = articles.filter(id__in=id_list)
        title = f'По запросу найдено новостей: {articles.count()}'

    if request.user.id:
        favorites = FavoriteArticle.objects.filter(user=request.user)
        fav_list = [0]
        for el in favorites:
            fav_list.append(el.article_id)
    else:
        fav_list = None

    a_count = len(articles)
    p = Paginator(articles, 2)
    p_number = request.GET.get('page')
    p_obj = p.get_page(p_number)
    context = {'articles': p_obj,
               'a_count': a_count,
               'favorites': fav_list,
               'title': title}
    return render(request, 'news/index.html', context)


def news_search(request, text, id):
    return news_index(request, text, id)


def news_user(request):
    articles = Article.objects.filter(author=request.user). \
        select_related('author'). \
        prefetch_related('tags'). \
        order_by('-date'). \
        annotate(Count('comments', distinct=True), Count('tags', distinct=True))
    context = {'articles': articles,
               'title': 'Мои новости'}
    return render(request, 'news/index.html', context)


def news_detail(request, id):
    article = Article.objects.select_related('author').get(id=id)
    comments = Comment.objects.select_related('author').filter(article=article).order_by('-date')
    images = Image.objects.filter(article=article)
    ip = get_ip(request)
    user = request.user if request.user.id else None
    ViewCount.objects.get_or_create(article=article, ip=ip, user=user)
    context = {'article': article,
               'comments': comments,
               'images': images}
    if request.method == 'POST':
        print(request.POST)
        if request.user.id:
            comment = Comment()
            comment.article = article
            comment.author = request.user
            comment.text = request.POST.get('text')
            comment.save()
            return redirect('news_detail', id)
        else:
            return redirect('login')
    return render(request, 'news/news.html', context)


def search_auto(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term', '')
        articles = Article.objects.filter(
            Q(title__icontains=q) | Q(author__username__icontains=q) | Q(tags__title__icontains=q)).distinct()
        results = []
        for a in articles:
            results.append(a.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
