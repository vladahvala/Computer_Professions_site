from django.core.files import File
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from ..models import Post, Category
from django.urls import reverse

# Перевірка створення постів та їх елементів
class PostTestCase(TestCase):
    def setUp(self):
        """Підготовка тестових даних."""
        self.image_path = 'D:\Computer_Professions_site\\blog\static\img\default.jpg'
        with open(self.image_path, 'rb') as img:
            self.image = SimpleUploadedFile(name='default.jpg', content=img.read(), content_type='image/jpg')
        # Створюємо категорію поста
        self.category = Category.objects.create(name="Default Category")
        # Створюємо тестовий пост
        self.post1 = Post.objects.create(title="Перший пост", text="Опис першого поста", category=self.category, img=self.image)

    def test_posts_page_loads(self):
        """Перевірка чи запускається сторінка із постами"""
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
    
    def test_post_creation(self):
        """Перевірка чи створено пост у базі даних"""
        # Перевіряємо чи пост був створений
        post_exists = Post.objects.filter(title="Перший пост").exists()
        self.assertTrue(post_exists)

         # Перевіряємо чи зображення поста завантажено
        post = Post.objects.get(title="Перший пост")
        self.assertIsNotNone(post.img)  # Перевіряємо, чи зображення не є порожнім
        self.assertTrue(os.path.exists(post.img.path))  # Перевіряємо чи файл зображення існує

        # Перевіряємо створення категорії поста
        self.assertEqual(post.category.name, "Default Category")
        # Перевіряємо створення опису поста
        self.assertEqual(post.text, "Опис першого поста")
    
    def test_post_str_method(self):
            """Перевіряємо метод __str__ для Post."""
            category = Category.objects.create(name="Test Category", category_slug="test-category")
            post = Post.objects.create(title="Test Post", text="Test content", category=category)
            self.assertEqual(str(post), "Test Post")


