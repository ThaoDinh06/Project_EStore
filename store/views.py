from django.shortcuts import render, redirect
from store.models import Category, SubCategory, Product
from django.db.models import Q
from store.my_module import *
from store.forms import FormUser, FormUserProfileInfo, FormContact
from cart.cart import Cart
from EStore.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMessage

# Phân trang
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# User authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# RSS
import feedparser


# SubCategory (Dùng chung)
subcategory_list = SubCategory.objects.order_by('name')


# Create your views here.
def index_2(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    # Đồ dùng nhà bếp
    category_ddnb = Category.objects.get(pk=2)

    # Thiết bị gia đình
    category_tbgd = Category.objects.get(pk=1)

    # Giỏ hàng
    cart = Cart(request)

    return render(request, 'store/index-2.html', {
        'category_ddnb': category_ddnb,
        'category_tbgd': category_tbgd,
        'session_status': session_status,
        'session_info': session_info,
        'cart': cart,
    })


def index(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    # Thiết bị gia đình
    subcategory_ttgd = SubCategory.objects.filter(category=1).values_list('id')
    list_subcategoryid_tbgd = []
    for item in subcategory_ttgd:
        list_subcategoryid_tbgd.append(item[0])
    list_product_tbgd = Product.objects.filter(subcategory__in=list_subcategoryid_tbgd).order_by('-public_day')[:21]

    # Đồ dùng nhà bếp
    subcategory_ddnb = SubCategory.objects.filter(category=2).values_list('id')
    list_subcategoryid_ddnb = []
    for item in subcategory_ddnb:
        list_subcategoryid_ddnb.append(item[0])
    list_product_ddnb = Product.objects.filter(subcategory__in=list_subcategoryid_ddnb).order_by('-public_day')[:21]

    # Giỏ hàng
    cart = Cart(request)

    return render(request, 'store/index.html', {
        'list_product_tbgd': list_product_tbgd,
        'list_product_ddnb': list_product_ddnb,
        'session_status': session_status,
        'session_info': session_info,
        'cart': cart,
    })


# def index(request):
#     # Đồ dùng nhà bếp
#     category_ddnb = Category.objects.get(pk=2)

#     # Thiết bị gia đình
#     category_tbgd = Category.objects.get(pk=1)

#     value = 1

#     print(request.COOKIES.get('visits'))
#     if request.COOKIES.get('visits'):
#         value = int(request.COOKIES.get('visits'))

#     response = render(request, 'store/index.html', {
#         'category_ddnb': category_ddnb,
#         'category_tbgd': category_tbgd,
#         'visits': value,
#     })

#     if value >= 1:
#         response.set_cookie('visits', value + 1)
#     else:
#         response.set_cookie('visits', value)
#     # response.delete_cookie('visits')

#     return response


def product_list(request, pk):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    # Products
    products = Product.objects.order_by('-public_day')
    if pk != 0:
        products = Product.objects.filter(subcategory_id=pk).order_by('-public_day')

    # Phân trang
    products_per_page = 15
    page = request.GET.get('page', 1)
    paginator = Paginator(products, products_per_page)

    try:
        products_pager = paginator.page(page)
    except PageNotAnInteger:
        products_pager = paginator.page(1)
    except EmptyPage:
        products_pager = paginator.page(paginator.num_pages)

    if pk == 0:
        list_product = Product.objects.order_by('-public_day')
        subcategory_name = 'Tất cả sản phẩm (' + str(len(list_product)) + ')'
    else:
        list_product = Product.objects.filter(subcategory=pk).order_by('-public_day')
        selected_subcategory = SubCategory.objects.get(pk=pk)
        subcategory_name = selected_subcategory.name + ' (' + str(len(list_product)) + ')'

    # Giỏ hàng
    cart = Cart(request)

    return render(request, 'store/product-list.html', {
        'subcategory_list': subcategory_list,
        'products': products_pager,
        'subcategory_name': subcategory_name,
        'session_status': session_status,
        'session_info': session_info,
        'cart': cart,
    })


def product_detail(request, pk):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    product = Product.objects.get(pk=pk)

    # Sản phẩm liên quan
    subcategoryid = product.subcategory_id
    # related_products = Product.objects.filter(Q(subcategory_id=subcategoryid)).order_by('-public_day')
    related_products = Product.objects.filter(subcategory=subcategoryid).exclude(id=pk).order_by('-public_day')

    # Lấy tên danh mục lên Breadcrumb
    subcategoryname = SubCategory.objects.get(id=subcategoryid)

    # Giỏ hàng
    cart = Cart(request)

    return render(request, 'store/product-detail.html', {
        'subcategory_list': subcategory_list,
        'product': product,
        'related_products': related_products,
        'session_status': session_status,
        'session_info': session_info,
        'subcategoryid': subcategoryid,
        'subcategoryname': subcategoryname,
        'cart': cart,
    })


def contact(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    # Giỏ hàng
    cart = Cart(request)

    # Liên hệ
    form = FormContact()
    result_contact = ''
    if request.POST.get('btnSendContact'):
        form = FormContact(request.POST)
        if form.is_valid():
            request.POST._mutable = True
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.phone_number = form.cleaned_data['phone_number']
            post.email = form.cleaned_data['email']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()

            # Gửi mail
            content = '<p>Chào bạn <b>' + post.name + '</b></p>'
            content += '<p>Chúng tôi đã nhận được thông tin của bạn thông quan Website EStore với nội dung như sau:</p>'
            content += '<p>' + post.message + '</p>'
            content += '<p>Chúng tôi sẽ liên hệ bạn trong thời gian sớm nhất.</p>'
            content += '<p>Trân trọng.</p>'

            # Không có html
            # send_mail(subject, content, EMAIL_HOST_USER, [email])

            # Có định dạng html
            msg = EmailMessage(post.subject, content, EMAIL_HOST_USER, [post.email])
            msg.content_subtype = 'html'
            msg.send()

            result_contact = '''
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    Gửi thông tin thành công. Cảm ơn bạn đã liên hệ. Chúng tôi sẽ phản hồi trong thời gian sớm nhất.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''
        else:
            result_contact = '''
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Gửi thông tin thất bại.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''

    return render(request, 'store/contact.html', {
        'session_status': session_status,
        'session_info': session_info,
        'cart': cart,
        'form': form,
        'result_contact': result_contact,
    })


def search(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    product_name = ''
    products_pager = []
    if request.GET.get('product_name'):
        # Gán biến
        product_name = request.GET.get('product_name')
        products_search = Product.objects.filter(name__contains=product_name).order_by('-public_day')

        # Phân trang
        products_per_page = 15
        page = request.GET.get('page', 1)
        paginator = Paginator(products_search, products_per_page)

        subcategory_name = str(len(products_search)) + ' sản phẩm với từ khóa "' + product_name + '"'
        list_product_sidebar = products_search

        try:
            products_pager = paginator.page(page)
        except PageNotAnInteger:
            products_pager = paginator.page(1)
        except EmptyPage:
            products_pager = paginator.page(paginator.num_pages)

    # Giỏ hàng
    cart = Cart(request)

    return render(request, 'store/product-list.html', {
        'products': products_pager,
        'subcategory_name': subcategory_name,
        'product_name': product_name,
        'session_status': session_status,
        'session_info': session_info,
        'cart': cart,
    })


def users(request):
    # Kiểm tra trạng thái đăng nhập của User
    session_status_users = check_session(request, 'sessionUser')
    session_info_users = ''
    if session_status_users:
        session_info_users = request.session.get('sessionUser')

    result_register = ''
    form_user = FormUser()
    form_profile = FormUserProfileInfo()
    if request.POST.get('btnRegister'):
        form_user = FormUser(request.POST)
        form_profile = FormUserProfileInfo(request.POST, request.FILES)
        if form_user.is_valid() and form_profile.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm_password']:
            # Lưu CSDL
            # User
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            # Profile
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()

            result_register = '''
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    Đăng ký thông tin thành công
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''
        else:
            result_register = '''
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Đăng ký thông tin thất bại
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''

    if request.POST.get('btnLogin'):
        # Gán biến
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['sessionUser'] = username
            return redirect('store:users')

    return render(request, 'store/users.html', {
        'form_user': form_user,
        'form_profile': form_profile,
        'result_register': result_register,
        'session_status_users': session_status_users,
        'session_info_users': session_info_users,
    })


def logout_user(request):
    logout(request)
    return redirect('store:users')


def read_rss(request):
    newsfeed = feedparser.parse('http://feeds.feedburner.com/bedtimeshortstories/LYCF')
    entry = newsfeed.entries[0]['title']
    print(entry)
    # print(entry.keys())

    return render(request, 'store/rss.html', {
        'newsfeed': newsfeed,
    })
