from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path(r'', views.blog_main), 
    path('searchpost/', views.search_post, name="search"),
    path('<slug>/', views.slug_process), #з <> дані передаються в views.blog_main
]
