from django.shortcuts import render, redirect
from .models import Post, Comment, Category
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import AddCommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView

# Create your views here.
#дані збираються з бази даних, відправляються на html-сторінку, потім рендеряться(готуються) і відправляються назад користувачу

def main(request, *args):
    page = request.GET.get('page')
    category = Category.objects.all()
    data_dict = {
        'category': category,
    }
    return render(request, 'main.html', data_dict)

"""def posts(request, *args):
    page = request.GET.get('page')
    posts = Post.objects.all()
    category = Category.objects.all()
    paginator = Paginator(posts, 4) #кількість постів, що відображаються на сторінці
    try:
        data_page = paginator.page(page)
    except PageNotAnInteger:
        data_page = paginator.page(1)
    except EmptyPage:
        data_page = paginator.page(paginator.num_pages)
    data_dict = {
        "slide_posts": posts,
        "posts": data_page,
        'category': category,
    }
    return render(request, 'posts.html', data_dict)#запит, адреса, словник із даними
    """

class PostListMain(ListView):
    model = Post              
    context_object_name = 'posts'
    template_name = 'posts.html'
    paginate_by = 4
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = Category.objects.all()
        context['slide_posts'] = Post.objects.all()
        return context
    
"""
def search_post(request):
    posts = None
    if request.method == "POST":
        text = request.POST.get("searchpost")#отримуємо ім'я інпута із html-файла
        posts = Post.objects.filter(Q(title__icontains=text.lower()) | Q(title__icontains=text.capitalize()) | Q(title__icontains=text.upper()))#шукаємо по полю title і lookup-пу icontains
    data_dict = { "posts": posts }
    return render(request, 'posts.html', data_dict)
"""

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
        context['sidebar'] = Category.objects.all()
        #form = get_comment_form(self.request, context['post'])
        return context


class PostSearchView(ListView):
    model = Post              
    context_object_name = 'query'
    template_name = 'navbar.html'

    def get_queryset(self):
        text = self.request.GET.get('searchposts')
        if text:
            object_list = self.model.objects.filter(Q(title__icontains=text.lower()) | Q(title__icontains=text.capitalize()) | Q(title__icontains=text.upper()))
        return object_list

    
def get_comment_form(request, post):
    """Post user commentary Form processing"""
    if request.method =="POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(post=post, content=content)
            comment.save()#зберігаємо об'єкт в базі данних
        return redirect(f'/{post.post_slug}')
    else:
        form = AddCommentForm()
    return form

'''def slug_process(request, slug):
    """Search URL in category slugs first and if no mathing
    Than searsh URL in post slugs
    In both cases show sidebar with categories"""
    category = Category.objects.all()
    categories = [ c.category_slug for c in category]
    if slug in categories:
        category_posts = Post.objects.filter(category__category_slug=slug)
        return render(request, "category.html", {
            "posts" : category_posts, 
            "category": category
        })


    post_slugs = [p.post_slug for p in Post.objects.all() ]
    if slug in post_slugs:
        post = Post.objects.get(post_slug = slug)
        comments = Comment.objects.filter(post=post) #змінна=елементові класу post
        form = get_comment_form(request, post)
        data_dict = { 'post': post, 
                      'comment_form': form,
                      'comments': comments,
                      'category': category,
                    }
        return render(request, 'post_view.html', data_dict)
'''

