from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path(r'', views.main), 
    path('posts/', views.PostListMain.as_view()), 
    path('searchpost/', views.PostListMain.as_view(), name="search"),
    path('post/<slug:slug>/', views.ShowPost.as_view(), name="post_url"),
    #path('<slug>/', views.slug_process), #з <> дані передаються в views.blog_main
]

