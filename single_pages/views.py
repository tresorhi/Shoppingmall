from django.shortcuts import render
from shop.models import Product

# Create your views here.
def homepage(request):
    recent_product = Product.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/homepage.html', {
        'recent_products': recent_product,
    })

def company(request):
    return render(request, 'single_pages/company.html')

def mypage(request):
    return render(request, 'single_pages/my_page.html')