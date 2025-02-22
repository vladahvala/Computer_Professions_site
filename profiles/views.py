from django.shortcuts import render
from .models import UserProfile
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from blog.forms import PostForm
from .forms import UpdateProfileForm
from blog.models import Post, Category
from django.shortcuts import redirect
from django.contrib import messages

def profile(request, pk):
    user_profile = get_object_or_404(UserProfile, profile_id=pk)
    posts = user_profile.post_set.all().order_by('-created_at')  # Додаємо сортування за датою (або інше поле)

    paginator = Paginator(posts, 4)  # Максимум 4 пости на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': user_profile,
        'page_obj': page_obj,  # Передаємо об'єкт пагінації
    }
    return render(request, 'profiles/profile.html', context)

def account(request):
    user = request.user
    user_account = getattr(user, 'userprofile', None)  

    if not user_account:
        return render(request, 'profiles/account.html', {'error': 'Profile not found'})

    # Log profile found
    print(f"Profile of user {user.username} found")

    posts = user_account.post_set.all().order_by('created_at')  

    if 'edit_bio' in request.path:  
        context = {
            'account': user_account,
            'posts': [],  
            'page_obj': None,  
        }
    else:
        paginator = Paginator(posts, 4) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'account': user_account,
            'page_obj': page_obj, 
        }

    return render(request, 'profiles/account.html', context)


# Функція для редагування посту
def edit_post(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)
    categories = Category.objects.all()

    if request.method == 'POST':
        # Копіюємо `POST`-дані в змінну, щоб видалити `post_slug`
        post_data = request.POST.copy()
        post_data['post_slug'] = post.post_slug  # Примусово встановлюємо старий slug

        form = PostForm(post_data, request.FILES, instance=post)  # Передаємо instance

        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успішно оновлено!')
            return redirect('account')
        else:
            for field, errors in form.errors.items():
                print(f"Помилка у {field}: {errors}")

    else:
        form = PostForm(instance=post)

    return render(request, 'profiles/edit_post.html', {
        'post': post,
        'form': form,
        'categories': categories,
        'post_slug': post_slug
    })

# Функція для видалення посту
def delete_post(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)
    post.delete()
    return redirect('account')  # Після видалення повертаємо на акаунт

# Функція для редагування посту
def UpdateProfile(request):
    profile = request.user.userprofile
    form = UpdateProfileForm(instance= profile)
    if request.method=='POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'You updated your Profile')
            return redirect('account')
    context = {'form': form}
    return render(request, 'profiles/updateprofile.html', context)

