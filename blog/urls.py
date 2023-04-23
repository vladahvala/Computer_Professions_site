from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path(r'', views.main), 
    path('posts/', views.PostListMain.as_view()), 
    path('searchpost/', views.PostSearchView.as_view(), name="search"),
    path('<slug>/', views.slug_process), #з <> дані передаються в views.blog_main
]
