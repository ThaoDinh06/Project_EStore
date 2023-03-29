from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from store.models import Product
from django.views.decorators.http import require_POST
from store.my_module import *


# Create your views here.
def cart_detail(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    # Giỏ hàng
    cart = Cart(request)

    # Xử lý cập nhật số lượng
    if request.POST.get('btnUpdateCart'):
        cart_new = {}
        for c in cart:
            quantity_new = int(request.POST.get('quantity2' + str(c['product'].pk)))
            if quantity_new != 0:
                product_new = {
                    str(c['product'].pk): {
                        'quantity': quantity_new,
                        'price': str(c['product'].price),
                        'coupon': '1'
                    }
                }
                cart_new.update(product_new)
            else:
                cart.remove(c['product'])
            c['quantity'] = quantity_new
        else:
            request.session['cart'] = cart_new

    return render(request, 'store/cart.html', {
        'cart': cart,
        'session_status': session_status,
        'session_info': session_info,
    })


@require_POST
def buy_now(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.POST.get('quantity'):
        cart.add(product=product, quantity=int(request.POST.get('quantity')))
    return redirect('cart:cart_detail')


@require_POST
def remove_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
