from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from news.models import Article
from .forms import ContactForm, UserAddForm
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


def profile_detail(request, id):
    profile = Profile.objects.select_related('user').get(user_id=id)
    f_count = FavoriteArticle.objects.filter(user=id).count()
    user = User.objects.get(id=id)
    user_info = [user.first_name, user.last_name, user.email,
                 profile.birthdate, profile.phone, profile.website, profile.github]
    complete = round(sum([bool(element) for element in user_info]) / len(user_info) * 100)
    context = {'profile': profile,
               'user': user,
               'complete': complete,
               'f_count': f_count,
               }
    return render(request, 'users/profile_detail.html', context)


@login_required(login_url='login')
def profile_update(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user),
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid() and user_form[0].is_valid():
            user_form[0].save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile', request.user.id)
        else:
            print(user_form[0].errors, profile_form.errors)
            messages.warning(request, user_form[0].errors)
            return redirect('profile_update')
    else:
        context = {'profile_form': ProfileUpdateForm(instance=profile),
                   'user_form': UserUpdateForm(instance=user)}
    return render(request, 'users/profile_update.html', context)


@login_required(login_url='login')
def profile_author(request):
    user = request.user
    group = Group.objects.get(name='Attention')
    user.groups.clear()
    user.groups.add(group)
    messages.success(request, 'Заявка на изменение прав принята')
    return redirect('profile', request.user.id)


@login_required(login_url='login')
def profile_delete(request):
    user = request.user
    user.delete()
    messages.success(request, 'Пользователь удален!')
    return redirect('news_index')


@login_required(login_url='login')
def password_update(request):
    user = request.user
    print(request.POST)
    form = PasswordChangeForm(user)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            password_info = form.save()
            update_session_auth_hash(request, password_info)
            messages.success(request, 'Пароль успешно обновлен!')
            return redirect('profile', user.id)

    context = {"form": form}
    return render(request, 'users/password.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print('Message send', form.cleaned_data)
        else:
            print(form.errors)
    else:
        form = ContactForm()
        form.name = 'test'
    context = {'form': form}
    return render(request, 'users/contact.html', context)


def register(request):
    if request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            group = Group.objects.get(name='Reader')
            user = form.save()
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, f'Пользователь {username} зарегистрирован!')
            Profile.objects.create(user=user, nickname=user.username)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile', user.id)
    else:
        form = UserAddForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required(login_url='login')
def profile_favorites(request, id):
    article = Article.objects.get(id=id)
    bookmark = FavoriteArticle.objects.filter(article=article, user=request.user)
    if bookmark.exists():
        bookmark.delete()
        messages.warning(request, f'Новость {article.title} удалена из закладок')
    else:
        FavoriteArticle.objects.create(user=request.user, article=article)
        messages.success(request, f'Новость {article.title} добавлена в закладки')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
