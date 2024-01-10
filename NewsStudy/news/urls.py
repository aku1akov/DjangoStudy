"""
URL configuration for NewsStudy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_index, name='news_index'),
    # path('user', views.news_user, name='news_user'),
    path('add', views.news_add, name='news_add'),
    path('search/<text>/<int:id>', views.news_search, name='news_search'),
    path('detail/<int:id>', views.news_detail, name='news_detail'),

    # path('search/tag/<int:id>', views.search_tag, name='search_tag'),
    # path('search/author/<int:id>', views.search_author, name='search_author'),

    path('search_auto/', views.search_auto, name='search_auto'),
    # path('<int:pk>/detail', views.ArticleDetailView.as_view(), name='detail_view'),
    path('update/<int:pk>', views.ArticleUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', views.ArticleDeleteView.as_view(), name='news_delete'),
]
