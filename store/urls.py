from django.urls import path
from store.views import *


app_name = 'store'
urlpatterns = [
    path('', index, name='index'),
    path('index-2/', index_2, name='index_2'),
    path('subcategory/<int:pk>/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('users/', users, name='users'),
    path('logout/', logout_user, name='logout_user'),
    path('rss/', read_rss, name='read_rss'),
]
