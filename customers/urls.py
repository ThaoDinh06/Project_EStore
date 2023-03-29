from django.urls import path
from customers.views import *


app_name = 'customers'
urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('my-account/', my_account, name='my_account'),
]
