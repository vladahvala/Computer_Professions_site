from django import forms
from django.contrib.auth.models import User
from .models import Comment
from django.contrib.auth.forms import UserCreationForm


class AddCommentForm(forms.ModelForm):
    content = forms.CharField(widget= forms.Textarea(attrs={'placeholder':'Comment here...', 'class':'form-control'}))
    #placeholder - текст, який пишеться перед тим як користувач ставить туди курсор
    class Meta:
        model = Comment
        fields = ['content']