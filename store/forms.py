from django import forms
from store import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from store.models import UserProfileInfo

phone_validator = RegexValidator(
    r"((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))", "Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx!")


class FormContact(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={
        'placeholder': 'Họ tên',
        'class': 'form-control'
    }))
    phone_number = forms.CharField(max_length=20, label='Phone', validators=[phone_validator],
                                   widget=forms.TextInput(attrs={
                                       'placeholder': 'Điện thoại',
                                       'class': 'form-control fh5co_contact_text_box',
                                       'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))',
                                       'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'
                                   }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control'
    }))
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={
        'placeholder': 'Tiêu đề',
        'class': 'form-control'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Nội dung',
        'class': 'form-control',
        'rows': '5'
    }))

    class Meta:
        model = models.Contact
        fields = '__all__'


class FormUser(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))
    confirm_password = forms.CharField(max_length=100, label='Confirm Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm Password"
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class FormUserProfileInfo(forms.ModelForm):
    portfolio = forms.URLField(required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Portfolio"
    }))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control-file",
    }))

    class Meta:
        model = UserProfileInfo
        exclude = ('user',)
