from django.urls import path
from . import views

urlpatterns = [  # IP주소/
    path('', views.homepage),
    path('about_company/', views.company),
    path('mypage/', views.mypage)
]