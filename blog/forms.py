from django import forms
from django.contrib.auth.models import User
from .models import Comment
from django.contrib.auth.forms import UserCreationForm

class AddCommentForm(forms.ModelForm):
    content = forms.CharField(widget= forms.Textarea(attrs={'placeholder':'Введіть коментар...', 'class':'form-control'}))
    class Meta:
        model = Comment
        fields = ['content']