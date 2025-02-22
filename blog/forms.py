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

from django import forms
from .models import Post, Category, UserProfile

class PostForm(forms.ModelForm):
    category = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'category-list', 'placeholder': 'Виберіть або введіть категорію'})
    )

    class Meta:
        model = Post
        fields = ('title', 'text', 'img', 'post_slug', 'category')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'post_slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_category(self):
        category_name = self.cleaned_data.get('category').strip()
        if not category_name:
            raise forms.ValidationError("Оберіть або введіть категорію.")

        category, created = Category.objects.get_or_create(name=category_name)
        return category

    def clean_post_slug(self):
        post_slug = self.cleaned_data.get('post_slug')
        post_id = getattr(self.instance, 'id', None)
        existing_post = Post.objects.filter(post_slug=post_slug).exclude(id=post_id)
        print(f"Existing post count: {existing_post.count()}")  # Debugging
        if existing_post.exists():
            raise forms.ValidationError('Цей slug вже зайнятий. Виберіть інший.')
        return post_slug


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.category = self.cleaned_data['category']
        if commit:
            instance.save()
        return instance