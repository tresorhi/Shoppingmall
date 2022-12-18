from django.shortcuts import render, redirect
from .models import Product, Category, Tag, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.
def delete_comment(request, pk):
    comment =  get_object_or_404(Comment, pk=pk)
    product = comment.product
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(product.get_absolute_url())
    else:
        PermissionDenied

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'hook_text', 'head_image', 'price', 'scissors', 'category', 'manufacturer']
    template_name = 'shop/product_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(ProductUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()  # 앞 뒤에 빈 공간 없애주는 명령
            tags_str = tags_str.replace(',', ';')
            tag_list = tags_str.split(';')
            for t in tag_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdate,self).get_context_data()
        if self.object.tags.exists:
            tag_str_list = list()
            for t in self.object.tags.all():
                tag_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tag_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_product_count'] = Product.objects.filter(category=None).count
        return context

class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    fields = ['name', 'hook_text', 'head_image', 'price', 'scissors', 'category', 'manufacturer']
    #모델면_form.html

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(ProductCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip() #앞 뒤에 빈 공간 없애주는 명령
                tags_str = tags_str.replace(',', ';')
                tag_list = tags_str.split(';')
                for t in tag_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/shop/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreate,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_product_count'] = Product.objects.filter(category=None).count
        return context

class ProductList(ListView):
    model = Product
    ordering = '-pk'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_product_count'] = Product.objects.filter(category=None).count
        return context


class ProductSearch(ProductList):  # ListView 상속, 모델명_list 형태로 데이터 전달, 템플릿도 모델명_list.html
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        product_list = Product.objects.filter(Q(title__contains=q) | Q(tags__name__contains=q)).distinct()
        return product_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context

class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_product_count'] = Product.objects.filter(category=None).count
        context['comment_form'] = CommentForm
        return context

def new_comment(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url()) #클라이언트에 서버가 할 일을 마지고 보내주는 정보
        else: #Get
            return redirect(product.get_absolute_url())
    else: #로그인 안 한 사용자
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def category_page(request, slug):
        if slug == 'no_category':
            category = "미분류"
            product_list = Product.objects.filter(category=None)
        else:
            category = Category.objects.get(slug=slug)
            product_list = Product.objects.filter(category=category)
        return render(request, 'shop/product_list.html', {
            'category' : category,
            'product_list' : product_list,
            'categories' : Category.objects.all(),
            'no_category_product_count' : Product.objects.filter(category=None).count
        })

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    product_list = tag.product_set.all()
    return render(request, 'shop/product_list.html', {
        'tag' : tag,
        'product_list' : product_list,
        'categories': Category.objects.all(),
        'no_category_product_count': Product.objects.filter(category=None).count
    })