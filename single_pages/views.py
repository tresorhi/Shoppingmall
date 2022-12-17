from django.shortcuts import render
#from blog.models import Post

# Create your views here.
def homepage(request):
    #recent_post = Post.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/homepage.html')
    #{'recent_posts' : recent_post,} 이게 html' 뒤에 콤마 찍고 있음
def company(request):
    return render(request, 'single_pages/company.html')