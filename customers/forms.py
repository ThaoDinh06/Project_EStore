from django import forms
from customers import models


class FormDangKy(forms.ModelForm):
    ho = forms.CharField(max_length=250, label='Họ', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Họ"
    }))
    ten = forms.CharField(max_length=250, label='Tên', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Tên"
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))
    mat_khau = forms.CharField(max_length=100, label='Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Mật khẩu"
    }))
    xac_nhan_mat_khau = forms.CharField(max_length=100, label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Xác nhận Mật khẩu"
    }))
    dien_thoai = forms.CharField(max_length=20, label='Điện thoại', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Điện thoại"
    }))
    dia_chi = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Địa chỉ",
        "rows": 4,
    }))

    class Meta:
        model = models.Customer
        # fields = '__all__'
        fields = ['ho', 'ten', 'email', 'mat_khau', 'dien_thoai', 'dia_chi']
