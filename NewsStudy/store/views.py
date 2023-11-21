from django.shortcuts import render


def index(request):
    context = {'title': 'Интернет магазин'}
    return render(request, 'store/index.html', context)
