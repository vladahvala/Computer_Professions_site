# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Post, Category
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.contrib.admin.sites import site


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder':'Введіть ім\'я...'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder':'Введіть пароль...'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder':'Підтвердіть пароль...'})

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'text', 'img')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control'}),
        }



    # def clean(self):
    #     cleaned_data = super().clean()
    #     category = cleaned_data.get('category')
    #     new_category = cleaned_data.get('new_category')

    #     # If a new category is provided, check if it already exists and create if not
    #     if new_category:
    #         if Category.objects.filter(name=new_category).exists():
    #             raise forms.ValidationError("This category already exists.")
    #         else:
    #             # Create new category and assign it to the form
    #             category = Category.objects.create(name=new_category)

    #     # If no category is selected and no new category is entered, raise an error
    #     if not category:
    #         raise forms.ValidationError("You must select or add a category.")
        
    #     cleaned_data['category'] = category
    #     return cleaned_data
