from django.db import models


# Create your models here.
class Customer(models.Model):
    ho = models.CharField(max_length=250, blank=False)
    ten = models.CharField(max_length=250, blank=False)
    email = models.EmailField(blank=False, unique=True)
    mat_khau = models.CharField(max_length=100, blank=False)
    dien_thoai = models.CharField(max_length=20)
    dia_chi = models.TextField()

    def __str__(self):
        return self.ho + ' ' + self.ten


