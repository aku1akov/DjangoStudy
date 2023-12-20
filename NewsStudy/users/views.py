from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib import messages
# Create your views here.


def profile(request):
    pass


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
            form.save()
            login = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            messages.success(request, f'Пользователь {login} зарегистрирован!')
            authenticate(username=login, password=pwd)
            return redirect('login')
    else:
        form = UserCreationForm(request.POST)
    context = {'form': form}
    return render(request, 'users/register.html', context)
