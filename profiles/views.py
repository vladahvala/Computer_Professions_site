from django.shortcuts import render
from .models import UserProfile

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import UserProfile

def profile(request, pk):
    user_profile = get_object_or_404(UserProfile, profile_id=pk)
    posts = user_profile.post_set.all()

    paginator = Paginator(posts, 4)  # Максимум 4 пости на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': user_profile,
        'page_obj': page_obj,  # Передаємо об'єкт пагінації
    }
    return render(request, 'profiles/profile.html', context)

def account(request):
    user_account = request.user.userprofile
    posts = user_account.post_set.all()

    paginator = Paginator(posts, 4)  # Maximum 4 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'account': user_account,
        'page_obj': page_obj,  # Passing the paginated posts to the template
    }
    return render(request, 'profiles/account.html', context)
