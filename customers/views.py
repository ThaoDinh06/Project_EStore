from django.shortcuts import render, redirect
from customers.forms import *
from customers.models import *
from store.my_module import *
from django.contrib.auth.hashers import Argon2PasswordHasher, PBKDF2PasswordHasher


# Create your views here.
def login(request):
    session_status = check_session(request, 'sessionKhachHang')
    if session_status:
        return redirect('customers:my_account')

    # Đăng ký
    form = FormDangKy()
    result_regiter = ''
    if request.POST.get('btnDangKy'):
        form = FormDangKy(request.POST, Customer)

        # Kiểm tra email tồn tại hay chưa?
        email = request.POST.get('email')
        khach_hang = Customer.objects.filter(email=email)
        if khach_hang.count() > 0:
            result_regiter = '''
                <div class="alert alert-warning alert-dismissible fade show" role="alert">
                    Email đã tồn tại. Vui lòng kiểm tra lại
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''
        else:
            if form.is_valid() and form.cleaned_data['mat_khau'] == form.cleaned_data['xac_nhan_mat_khau']:
                # hasher = Argon2PasswordHasher()  # salt: 8 bytes
                hasher = PBKDF2PasswordHasher()  # salt: 1 bytes
                request.POST._mutable = True
                post = form.save(commit=False)
                post.ho = form.cleaned_data['ho']
                post.ten = form.cleaned_data['ten']
                post.email = form.cleaned_data['email']
                post.mat_khau = hasher.encode(form.cleaned_data['mat_khau'], '123')
                post.dien_thoai = form.cleaned_data['dien_thoai']
                post.dia_chi = form.cleaned_data['dia_chi']
                post.save()
                result_regiter = '''
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    Đăng ký thông tin thành công.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''
    # Đăng nhập
    result_login = ''
    if request.POST.get('btnDangNhap'):
        # Gán biến
        email = request.POST.get('email')
        mat_khau = request.POST.get('mat_khau')
        hasher = PBKDF2PasswordHasher()
        encoded = hasher.encode(mat_khau, '123')

        # Đọc dữ liệu từ DB
        khach_hang = Customer.objects.filter(email=email, mat_khau=encoded)
        if khach_hang.count() > 0:
            # Tạo session đăng nhập của khách hàng
            request.session['sessionKhachHang'] = khach_hang.values()[0]  # dict
            return redirect('store:index')
        else:
            result_login = '''
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Đăng nhập thất bại.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''

    return render(request, 'store/login.html', {
        'form': form,
        'result_regiter': result_regiter,
        'result_login': result_login,
    })


def my_account(request):
    session_status = check_session(request, 'sessionKhachHang')
    if not session_status:
        return redirect('customers:login')

    return render(request, 'store/my-account.html')


def logout(request):
    if request.session.get('sessionKhachHang'):
        del request.session['sessionKhachHang']
    return redirect('customers:login')
