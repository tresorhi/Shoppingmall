from allauth.socialaccount.templatetags import socialaccount
from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

class Manufacturer(models.Model):
    #서버 이름
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    nickname = models.CharField(max_length=100) # 아이템 소유자 아이디
    phone_num = models.CharField(max_length=100) # 연락처
    addr = models.CharField(max_length=100) # 마을

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/manufacturer/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Manufacturers'