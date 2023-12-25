from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.


def profile(request):
    return render(request, 'users/profile.html')


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


def users_index(request):
    if request.method == 'POST':
        print(request.POST.get('login'))
    # print(request.user, request.user.id)
    # user_acc = Account.objects.get(user=request.user)
    # print(user_acc.birthdate, user_acc.gender)
    return render(request, 'users/auth.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            category = request.POST['account_type']
            if category == 'author':
                group = Group.objects.get(name='ActionsRequired')
            else:
                group = Group.objects.get(name='Reader')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, f'Пользователь {username} зарегистрирован!')
            Profile.objects.create(user=user, nickname=user.username)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('news_index')
    else:
        form = UserCreationForm(request.POST)
    context = {'form': form}
    return render(request, 'users/register.html', context)
