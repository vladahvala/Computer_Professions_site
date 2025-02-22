from django import forms
from django.forms import ModelForm
from .models import UserProfile

class UpdateProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        labels = {
            'name': 'Ім\'я',
            'email': 'Поштова адреса',
            'username': 'Ім\'я користувача',
            'profession': 'Професія',
            'picture': 'Аватар',
            'avatar': 'Аватар',
            'about': 'Про себе',
        }
        widgets = {
            'about': forms.Textarea(attrs={
                'style': 'height:100px;'  
            }),
        }