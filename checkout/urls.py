from django.urls import path
from checkout.views import *


app_name = 'checkout'
urlpatterns = [
    path('checkout/', checkout, name='checkout'),
]
