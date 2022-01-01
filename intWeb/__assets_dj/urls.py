from django.urls import path, re_path,include
# re_path方法相当于 django1.11 url正则表达式
from . import views

# 载入视图模块

app_name = 'asset'
# 设置应用命名空间

urlpatterns = [
    path('', views.index, name="index" ),

    path('dashboard', views.dashboard, name="dashboard" ),
    path('cabinet/', views.cabinet.as_view(), name='cabinet'),
    path('assets/', views.assets.as_view(), name='assets'),
    re_path(r'^detail/', views.assetDetail.as_view(), name='detail'),
    re_path(r'^getCorp/', views.getCorp.as_view(), name='getCorp'),
    # re_path(r'^search/$', views.search, name='search'),

    ]
