"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from news.views import *
from vocabulary.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # News
    path(r'api/v1/news/<uuid:news_id>', get_news_detail, name='news_detail'),
    path(r'api/v1/news/<uuid:news_id>/view', get_news_view, name='news_html'),
    # Categories
    path(r'api/v1/category', get_all_categories, name='list_categories'),
    path(r'api/v1/category/<str:category_name>', get_news_by_category, name='news_by_category'),
    # Vocabulary
    path(r'api/v1/vocabulary', get_all_words, name='list_vocabulary'),
    path(r'api/v1/target', get_all_targets, name='list_target'),
    path(r'api/v1/field', get_all_fields, name='list_field'),
]
