from django.contrib import admin
from store.models import UserProfileInfo, Category, SubCategory, Product


# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)