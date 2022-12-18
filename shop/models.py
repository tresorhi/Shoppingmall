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

class Product(models.Model):
    name = models.CharField(max_length=50)
    hook_text = models.CharField(max_length=100, blank=True)


    head_image = models.ImageField(upload_to='shop/images/%Y/%m/%d/', blank=True)
    # %Y 2022, %y 22

    price = models.IntegerField(default=1)
    scissors = models.IntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    #다대일 관계
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.SET_NULL)

    #다대다 관계
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.name}::{self.author} : {self.created_at}'

    def get_absolute_url(self):
        return f'/shop/{self.pk}/'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.product.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'
