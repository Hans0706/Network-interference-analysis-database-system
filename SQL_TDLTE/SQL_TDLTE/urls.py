"""SQL_TDLTE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlp atterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TDLTE.views import *
urlpatterns = [
    path('index/', index, name='index'),
    path('index/login/',login,name='login'),
    path('index/regist/',regist,name='regist'),
    # path('main/',main,name='main'),
    path('index/jump00/',search_page00,name='jump1'),
    path('index/jump01/',search_page01,name='jump1'),
    path('index/jump08/',search_page08,name='jump8'),
    path('index/jump1/',search_page1,name='jump1'),
    path('index/jump2/',search_page2,name='jump2'),
    path('index/jump3/',search_page3,name='jump3'),
    path('index/jump4/',search_page4,name='jump4'),
    path('index/jump4_2/',search_page4_2,name='jump4_2'),
    path('index/jump5/', search_page5, name='jump4'),
    path('index/jump6/', search_page6, name='jump4'),
    path('index/search1/',search_data_1,name='search1'),
    path('index/search2/',search_data_2,name='search2'),
    path('index/search3/',search_data_3,name='search3'),
    path('index/search4_1/',search_data_4_1,name='search4_1'),
    path('index/search4_2/',search_data_4_2,name='search4_2'),
    path('index/analyze_1/',analyze_data_1,name='analyze_1'),
    path('index/analyze_2/',analyze_data_2,name='analyze_2'),
    path('index/interrupt/',search_interupt,name='interrupt'),
    path('index/loadData/', import_data, name='loadData'),
    path('index/exportData/', export_data, name='exportData'),
    path('index/p/', get_progress, name="data_fresh"),
]
