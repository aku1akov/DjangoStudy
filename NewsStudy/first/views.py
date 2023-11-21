from django.shortcuts import render


def index(request):
    return render(request, 'first/index.html')


def custom_404(request, exception):
    return render(request, 'first/err404.html')
