from django.test import TestCase
from django.core.files import File
from django.urls import reverse
from ..models import Post, Category
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

class MainViewTestCase(TestCase):
    def setUp(self):
        """Підготовка тестових даних."""
        # Створюємо категорії
        self.category1 = Category.objects.create(name="Category 1", category_slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", category_slug="category-2")
        
        # Створюємо пости
        self.post1 = Post.objects.create(title="Post 1", text="Text 1", category=self.category1)
        self.post2 = Post.objects.create(title="Post 2", text="Text 2", category=self.category2)
        
        # Створюємо тестового користувача
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_main_page_logged_in(self):
        """Перевірка, чи завантажується головна сторінка для залогінених користувачів."""
        self.client.login(username='testuser', password='password')  # Логін користувача
        response = self.client.get(reverse('main'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertIn('category', response.context)
        self.assertEqual(len(response.context['category']), 2)

    def test_main_page_not_logged_in(self):
        """Перевірка, чи переадресовує на сторінку входу, якщо користувач не залогінений."""
        response = self.client.get(reverse('main'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('main'))


class PostListMainViewTestCase(TestCase):
    def setUp(self):
        """Підготовка тестових даних."""
        self.category = Category.objects.create(name="Test Category", category_slug="test-category")
        self.post1 = Post.objects.create(title="Post 1", text="Text 1", category=self.category)
        self.post2 = Post.objects.create(title="Post 2", text="Text 2", category=self.category)
        self.post3 = Post.objects.create(title="Another Post", text="Text 3", category=self.category)

        # Створюємо тестового користувача та логінимо його
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_post_list_main_page(self):
        """Перевірка відображення списку постів для залогінених користувачів."""
        self.client.login(username='testuser', password='password')  # Логін користувача
        response = self.client.get(reverse('search'))  # Ваше ім'я маршруту для `PostListMain`
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')
        self.assertEqual(len(response.context['posts']), 3)  # Перевіряємо, чи всі пости відображаються
        self.assertIn('slide_posts', response.context)
        self.assertIn('category', response.context)

    def test_post_search(self):
        """Перевірка пошуку постів для залогінених користувачів."""
        self.client.login(username='testuser', password='password')  # Логін користувача
        response = self.client.get(reverse('search') + "?searchpost=Post")
        self.assertEqual(response.status_code, 200)
        posts = response.context['posts']
        self.assertEqual(len(posts), 3)  # Має бути три пости, які містять "Post" у назві
        for post in posts:
            self.assertIn("Post", post.title)

    def test_post_list_not_logged_in(self):
        """Перевірка, чи користувач буде переадресований на сторінку входу, якщо він не залогінений."""
        response = self.client.get(reverse('main'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('main'))

class CategoryListMainViewTestCase(TestCase):
    def setUp(self):
        """Підготовка тестових даних."""
        # Створюємо категорії
        self.category1 = Category.objects.create(name="Category 1", category_slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", category_slug="category-2")
        
        # Створюємо пости
        self.post1 = Post.objects.create(title="Post 1", text="Text 1", category=self.category1)
        self.post2 = Post.objects.create(title="Post 2", text="Text 2", category=self.category1)
        self.post3 = Post.objects.create(title="Post 3", text="Text 3", category=self.category2)

        # Створюємо тестового користувача та логінимо його
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_category_post_list(self):
        """Перевірка фільтрації постів за категорією для залогінених користувачів."""
        self.client.login(username='testuser', password='password')  # Логін користувача
        response = self.client.get(reverse('category_list_main', kwargs={'category_slug': 'category-1'}))
        
        self.assertEqual(response.status_code, 200)
        posts = response.context['posts']
        
        # Перевіряємо, чи всі пости з категорії "category-1"
        self.assertEqual(len(posts), 2)  # Має бути два пости з категорії 1
        for post in posts:
            self.assertEqual(post.category.category_slug, 'category-1')

        # Перевірка наявності категорії в контексті
        self.assertIn('selected_category', response.context)
        self.assertEqual(response.context['selected_category'], self.category1)

    def test_post_list_not_logged_in(self):
        """Перевірка, чи користувач буде переадресований на сторінку входу, якщо він не залогінений."""
        response = self.client.get(reverse('main'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('main'))

class ShowPostViewTestCase(TestCase):
    def setUp(self):
        """Підготовка тестових даних."""
        # Створюємо категорію
        self.category = Category.objects.create(name="Test Category", category_slug="test-category")
        
        # Створюємо пост
        self.post = Post.objects.create(title="Test Post", text="Test Content", category=self.category, post_slug="test-post")

        # Створюємо тестового користувача та логінимо його
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_show_post_view(self):
        """Перевірка відображення окремого поста для залогінених користувачів."""
        self.client.login(username='testuser', password='password')  # Логін користувача
        response = self.client.get(reverse('post_url', kwargs={'slug': 'test-post'}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_view.html')
        self.assertEqual(response.context['post'].title, "Test Post")
        self.assertEqual(response.context['post'].text, "Test Content")
        self.assertEqual(response.context['post'].category.name, "Test Category")
        
        # Перевірка, чи є категорії в контексті
        self.assertIn('category', response.context)
        self.assertEqual(len(response.context['category']), 1)  # Має бути лише одна категорія

    def test_post_list_not_logged_in(self):
        """Перевірка, чи користувач буде переадресований на сторінку входу, якщо він не залогінений."""
        response = self.client.get(reverse('main'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('main'))


class PaginationTestCase(TestCase):
    def setUp(self):
        """Підготовка тестових даних для перевірки пагінації."""
        self.category = Category.objects.create(name="Test Category")
        self.num_posts = 10  # Загальна кількість постів
        self.posts_per_page = 4  # Кількість постів на сторінці (за замовчуванням у вашому `PostListMain`)

        # Створюємо 10 постів
        for i in range(self.num_posts):
            Post.objects.create(
                title=f"Post {i + 1}",
                text=f"Content for post {i + 1}",
                category=self.category,
            )

        # Створення користувача для тестування
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_pagination_limit(self):
        """Перевіряємо, чи кількість постів на сторінці відповідає обмеженню."""
        # Логін користувача перед запитом
        self.client.login(username='testuser', password='password')
        
        response = self.client.get(reverse('posts'))  # Замініть на вашу правильну URL-іменну
        self.assertEqual(response.status_code, 200)

        # Перевіряємо, що на першій сторінці рівно `posts_per_page` постів
        posts_on_page = response.context['posts']  # `posts` - ваш `context_object_name`
        self.assertEqual(len(posts_on_page), self.posts_per_page)

    def test_pagination_total_pages(self):
        """Перевіряємо, чи кількість сторінок обчислена правильно."""
        self.client.login(username='testuser', password='password')
        
        response = self.client.get(reverse('posts'))  # Замініть на вашу правильну URL-іменну
        self.assertEqual(response.status_code, 200)

        # Загальна кількість сторінок
        paginator = response.context['paginator']
        total_pages = paginator.num_pages
        self.assertEqual(total_pages, (self.num_posts // self.posts_per_page) + 1)

    def test_pagination_next_page(self):
        """Перевіряємо перехід на наступну сторінку."""
        self.client.login(username='testuser', password='password')
        
        response = self.client.get(reverse('posts') + '?page=2')
        self.assertEqual(response.status_code, 200)

        # Перевірка кількості постів на другій сторінці
        posts_on_page = response.context['posts']
        self.assertEqual(len(posts_on_page), self.posts_per_page)

    def test_invalid_page_number(self):
        """Перевіряємо обробку некоректного номера сторінки."""
        self.client.login(username='testuser', password='password')
        
        response = self.client.get(reverse('posts') + '?page=999')
        self.assertEqual(response.status_code, 404)  # Або інший код відповіді, який ви використовуєте для помилкових сторінок









