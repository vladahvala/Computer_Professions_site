from django.test import TestCase
from django.core.files import File
from django.urls import reverse
from ..models import Post, Category
from django.core.files.uploadedfile import SimpleUploadedFile

class MainViewTestCase(TestCase):
    def setUp(self):
        """Підготовка тестових даних."""
        # Створюємо категорії
        self.category1 = Category.objects.create(name="Category 1", category_slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", category_slug="category-2")
        
        # Створюємо пости
        self.post1 = Post.objects.create(title="Post 1", text="Text 1", category=self.category1)
        self.post2 = Post.objects.create(title="Post 2", text="Text 2", category=self.category2)

    def test_main_page(self):
        """Перевірка, чи завантажується головна сторінка."""
        response = self.client.get(reverse('main'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertIn('category', response.context)
        self.assertEqual(len(response.context['category']), 2)

class PostListMainViewTestCase(TestCase):
    def setUp(self):
        """Підготовка тестових даних."""
        self.category = Category.objects.create(name="Test Category", category_slug="test-category")
        self.post1 = Post.objects.create(title="Post 1", text="Text 1", category=self.category)
        self.post2 = Post.objects.create(title="Post 2", text="Text 2", category=self.category)
        self.post3 = Post.objects.create(title="Another Post", text="Text 3", category=self.category)

    def test_post_list_main_page(self):
        """Перевірка відображення списку постів."""
        response = self.client.get(reverse('search'))  # Ваше ім'я маршруту для `PostListMain`
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')
        self.assertEqual(len(response.context['posts']), 3)  # Перевіряємо, чи всі пости відображаються
        self.assertIn('slide_posts', response.context)
        self.assertIn('category', response.context)

    def test_post_search(self):
        """Перевірка пошуку постів."""
        response = self.client.get(reverse('search') + "?searchpost=Post")
        self.assertEqual(response.status_code, 200)
        posts = response.context['posts']
        self.assertEqual(len(posts), 3)  # Має бути три пости, які містять "Post" у назві
        for post in posts:
            self.assertIn("Post", post.title)

class CategoryListMainViewTestCase(TestCase):
    def setUp(self):
        """Підготовка тестових даних."""

        self.category1 = Category.objects.create(name="Category 1", category_slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", category_slug="category-2")
        self.post1 = Post.objects.create(title="Post 1", text="Text 1", category=self.category1)
        self.post2 = Post.objects.create(title="Post 2", text="Text 2", category=self.category1)
        self.post3 = Post.objects.create(title="Post 3", text="Text 3", category=self.category2)

    def test_category_post_list(self):
        """Перевірка фільтрації постів за категорією."""
        response = self.client.get(reverse('category_list_main', kwargs={'category_slug': 'category-1'}))
        self.assertEqual(response.status_code, 200)
        posts = response.context['posts']
        self.assertEqual(len(posts), 2)  # Має бути два пости з категорії 1
        for post in posts:
            self.assertEqual(post.category.category_slug, 'category-1')

class ShowPostViewTestCase(TestCase):
    def setUp(self):
        """Підготовка тестових даних."""
        self.category = Category.objects.create(name="Test Category", category_slug="test-category")
        self.post = Post.objects.create(title="Test Post", text="Test Content", category=self.category, post_slug="test-post")

    def test_show_post_view(self):
        """Перевірка відображення окремого поста."""
        response = self.client.get(reverse('post_url', kwargs={'slug': 'test-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_view.html')
        self.assertEqual(response.context['post'].title, "Test Post")
        self.assertEqual(response.context['post'].text, "Test Content")
        self.assertEqual(response.context['post'].category.name, "Test Category")

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

    def test_pagination_limit(self):
        """Перевіряємо, чи кількість постів на сторінці відповідає обмеженню."""
        response = self.client.get(reverse('posts'))  # Замініть на вашу URL-іменну
        self.assertEqual(response.status_code, 200)

        # Перевіряємо, що на першій сторінці рівно `posts_per_page` постів
        posts_on_page = response.context['posts']  # `posts` - ваш `context_object_name`
        self.assertEqual(len(posts_on_page), self.posts_per_page)

    def test_pagination_total_pages(self):
        """Перевіряємо, чи кількість сторінок обчислена правильно."""
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)

        # Загальна кількість сторінок
        paginator = response.context['paginator']
        total_pages = paginator.num_pages
        self.assertEqual(total_pages, (self.num_posts // self.posts_per_page) + 1)

    def test_pagination_next_page(self):
        """Перевіряємо перехід на наступну сторінку."""
        response = self.client.get(reverse('posts') + '?page=2')
        self.assertEqual(response.status_code, 200)

        # Перевірка кількості постів на другій сторінці
        posts_on_page = response.context['posts']
        
        # Оскільки на першій сторінці буде 4 пости, на другій повинно бути 4
        expected_posts_second_page = self.num_posts - self.posts_per_page  # Після першої сторінки залишиться 6 постів
        expected_posts_last_page = self.num_posts - (self.posts_per_page * (self.num_posts // self.posts_per_page))

        # Перевірка, чи кількість постів на другій сторінці відповідає очікуваній
        self.assertEqual(len(posts_on_page), self.posts_per_page)

        # Перевірка кількості постів на останній сторінці
        response_last_page = self.client.get(reverse('posts') + '?page=3')
        posts_on_last_page = response_last_page.context['posts']

        self.assertEqual(len(posts_on_last_page), expected_posts_last_page)

    def test_invalid_page_number(self):
        """Перевіряємо обробку некоректного номера сторінки."""
        response = self.client.get(reverse('posts') + '?page=999')
        self.assertEqual(response.status_code, 404)  # Або інший код відповіді, який ви використовуєте для помилкових сторінок
