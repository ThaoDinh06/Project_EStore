from django.shortcuts import render, redirect
from cart.cart import Cart
from store.my_module import *
from checkout.models import Order, OrderItem
# Email
from EStore.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMessage


# Create your views here.
def checkout(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')
    else:
        return redirect('cart:cart_detail')

    # Giỏ hàng
    cart = Cart(request)

    # Ghi vào CSDL
    order = Order()
    if request.POST.get('btnOrder'):
        order.username = session_info['email']
        order.first_name = session_info['ten']
        order.last_name = session_info['ho']
        order.phone = session_info['dien_thoai']
        order.address = session_info['dia_chi']
        order.total = cart.get_final_total_price()
        order.save()

        # Chi tiết đơn hàng
        for c in cart:
            OrderItem.objects.create(order=order,
                                     product=c['product'],
                                     price=c['price'],
                                     quantity=c['quantity'])

        # Gửi email
        email_address = order.username
        subject = 'Xác nhận đơn hàng ' + str(order.id)
        message = 'Cảm ơn quý khách <b>' + order.last_name + ' ' + order.first_name + \
                  '</b> đã đặt hàng tại EStore. Danh sách các sản phẩm đã đặt như sau:<br>'

        message += '''
        <table class="table">
            <thead class="thead-light">
                <tr>
                    <th scope="col">STT</th>
                    <th scope="col">Tên sản phẩm</th>
                    <th scope="col">Số lượng</th>
                    <th scope="col">Đơn giá</th>
                    <th scope="col">Thành tiền</th>
                </tr>
            </thead>
            <tbody>'''
        for c in cart:
            message += '''<tr>
                <th scope="row">1</th>
                <td>''' + str(c['product']) + '''</td>
                <td>''' + str(c['quantity']) + '''</td>
                <td>''' + str(c['product'].price) + '''</td>
                <td>''' + str(c['total_price']) + '''</td>
            </tr>'''
        message += '''</tbody>
        </table>
        '''

        msg = EmailMessage(subject, message, EMAIL_HOST_USER, [email_address])
        msg.content_subtype = 'html'
        msg.send()

        # Xóa giỏ hàng sau khi đặt hàng thành công
        cart.clear()

        return render(request, 'store/result.html', {
            'cart': cart,
            'session_status': session_status,
            'session_info': session_info,
        })

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'session_status': session_status,
        'session_info': session_info,
    })
