from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path(r'', views.main, name="main"), 
    path('posts/', views.PostListMain.as_view(), name="posts"),
    path('searchpost/', views.PostListMain.as_view(), name="search"),
    path('<slug:category_slug>/', views.CategoryListMain.as_view(), name='category_list_main'), 
    path('post/<slug:slug>/', views.ShowPost.as_view(), name="post_url")
]

