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
from .models import Post, Category

class PostForm(forms.ModelForm):
    existing_category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Оберіть категорію",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    new_category = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Або введіть нову категорію'})
    )

    class Meta:
        model = Post
        fields = ('title', 'text', 'img', 'post_slug', 'existing_category', 'new_category')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'post_slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        existing_category = cleaned_data.get('existing_category')
        new_category = cleaned_data.get('new_category')

        if existing_category and new_category:
            raise forms.ValidationError("Виберіть існуючу категорію або введіть нову, але не обидва варіанти одночасно.")

        if not existing_category and not new_category:
            raise forms.ValidationError("Оберіть існуючу категорію або введіть нову.")

        return cleaned_data

    def clean_post_slug(self):
        post_slug = self.cleaned_data.get('post_slug')
        
        # Check if the slug already exists
        if Post.objects.filter(post_slug=post_slug).exists():
            raise forms.ValidationError('Цей slug вже зайнятий. Виберіть інший.')

        return post_slug

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_category_name = self.cleaned_data.get('new_category')

        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            instance.category = category
        else:
            instance.category = self.cleaned_data.get('existing_category')

        if commit:
            instance.save()
        return instance


