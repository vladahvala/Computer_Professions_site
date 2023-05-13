from django.shortcuts import render, redirect
from .models import Post, Category
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView


def main(request, *args):
    page = request.GET.get('page')
    category = Category.objects.all()
    data_dict = {
        'category': category,
    }
    return render(request, 'main.html', data_dict)

class PostListMain(ListView):
    model = Post              
    context_object_name = 'posts'
    template_name = 'posts.html'
    paginate_by = 4
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slide_posts'] = Post.objects.all()
        context['category'] = Category.objects.all()
        return context
    def get_queryset(self):       
        search_query = self.request.GET.get("searchpost")
        if search_query:
            return Post.objects.filter(
                                    Q(title__icontains=search_query.lower()) | 
                                    Q(title__icontains=search_query.upper()) | 
                                    Q(title__icontains=search_query.capitalize())
                                )
        return Post.objects.all()  

'''
class  CategoryListMain(ListView):
    model = Category
    template_name = "category.html"
    context_object_name = 'post'
    paginate_by = 4
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['category_slug']
        context['category'] = Category.objects.filter(category_slug=slug)
        return context
'''

class ShowPost(DetailView):
    model = Post
    template_name = "post_view.html"
    slug_url_kwarg = "slug"
    context_object_name = 'post'
    def get_object(self):
        slug = self.kwargs['slug']
        obj_post = Post.objects.get(post_slug = slug)
        return obj_post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

