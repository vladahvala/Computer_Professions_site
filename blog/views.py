from django.shortcuts import render, redirect
from .models import Post, Category
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView
from .forms import CustomUserCreationForm
from .forms import PostForm

def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')

    return render(request, 'login_register.html', {'page':page})

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # встановлення пароля
            user.save()  # збереження користувача в базу даних

            # Тепер ми можемо аутентифікувати користувача з новим паролем
            user = authenticate(request, username=user.username, password=request.POST['password1'])
            
            if user is not None:
                login(request, user)  # авторизація користувача
                return redirect('main')  # перенаправлення на головну сторінку

    context = {'form': form, 'page': page}
    return render(request, 'login_register.html', context)



@login_required(login_url='login') 
def main(request, *args):
    page = request.GET.get('page')
    category = Category.objects.all()
    data_dict = {
        'category': category,
    }
    return render(request, 'main.html', data_dict)

class PostListMain(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slide_posts'] = Post.objects.all().order_by('id')  # Додаємо сортування для slide_posts
        context['category'] = Category.objects.all()
        return context

    def get_queryset(self):
        search_query = self.request.GET.get("searchpost")
        queryset = Post.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query.lower()) |
                Q(title__icontains=search_query.upper()) |
                Q(title__icontains=search_query.capitalize())
            )

        return queryset.order_by('id')  # Завжди сортуємо за 'id'



class CategoryListMain(LoginRequiredMixin, ListView):
    model = Post
    template_name = "category.html"
    context_object_name = 'posts'
    paginate_by = 4
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context
    def get_queryset(self):
        slug = self.kwargs['category_slug']
        if slug:
            objects = Post.objects.filter(category__category_slug = slug)
            print(objects)
            return objects


class ShowPost(LoginRequiredMixin, DetailView):
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
        context['category'] = Category.objects.all()
        return context
    
class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "add_post.html"

    def form_valid(self, form):
        # The form is valid, so we just save the post as usual
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()  # Provide existing categories to the template
        return context