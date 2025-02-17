from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>', views.profile, name= 'profile'),
    path('account', views.account, name='account')
]