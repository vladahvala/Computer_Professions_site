from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path(r'', views.main), 
    path('posts/', views.posts), 
    path('searchpost/', views.search_post, name="search"),
    path('<slug>/', views.slug_process), #з <> дані передаються в views.blog_main
]
