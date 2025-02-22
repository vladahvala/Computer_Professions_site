from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>', views.profile, name= 'profile'),
    path('account', views.account, name='account'),
    path('post/<str:post_slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<str:post_slug>/delete/', views.delete_post, name='delete_post'),
    path('updateprofile', views.UpdateProfile, name='updateprofile'),  
]