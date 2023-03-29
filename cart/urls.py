from django.urls import path
from cart.views import *


app_name = 'cart'
urlpatterns = [
    path('cart/', cart_detail, name='cart_detail'),
    path('buy_now/<int:product_id>/', buy_now, name='buy_now'),
    path('remove_cart/<int:product_id>/', remove_cart, name='remove_cart'),
]
