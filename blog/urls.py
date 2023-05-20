from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path(r'', views.main), 
    path('posts/', views.PostListMain.as_view()),
    path('searchpost/', views.PostListMain.as_view(), name="search"),
    path('<slug:category_slug>/', views.CategoryListMain.as_view()),  
    path('post/<slug:slug>/', views.ShowPost.as_view(), name="post_url")
]

