from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from ..models import Post, Category

class PostTestCase(TestCase):
    
    def setUp(self):
        """Підготовка тестових даних."""
        # Створюємо категорію поста
        self.category = Category.objects.create(name="Default Category")
        # Створюємо тестовий пост
        self.post1 = Post.objects.create(title="Перший пост", text="Опис першого поста", category=self.category)
        
        # Створюємо тестового користувача
        self.user = User.objects.create_user(username="testuser", password="testpassword")
    
    def test_posts_page_loads(self):
        """Перевірка чи запускається сторінка із постами після авторизації"""
        # Логін користувача
        self.client.login(username="testuser", password="testpassword")
        
        # Робимо GET запит на сторінку постів
        response = self.client.get(reverse('posts'))  # Замініть 'posts' на правильну URL-іменну
        
        # Перевіряємо, чи сторінка завантажується без помилок
        self.assertEqual(response.status_code, 200)
    
    def test_post_creation(self):
        """Перевірка чи створено пост у базі даних"""
        # Логін користувача
        self.client.login(username="testuser", password="testpassword")
        
        # Перевіряємо, чи пост був створений
        post_exists = Post.objects.filter(title="Перший пост").exists()
        self.assertTrue(post_exists)

    def test_get_absolute_url(self):
        """Перевірка, чи працює get_absolute_url для постів"""
        post = Post.objects.create(title="Test Post", text="Test content", category=self.category)
        self.assertEqual(post.get_absolute_url(), reverse('post_url', args=[post.post_slug]))

