from django.db import models
from django.utils import timezone
from PIL import Image #pillow - бібліотека для роботи із зображеннями
from django.contrib.auth.models import User

#makemigrations - створює інструкції для додавання нової таблиці в базу даних
#migrate - виконує ці інструкції

#Post - публікація. кожен ряд в таблиці - відомості про 1 публікацію
    #кожна його властивість - колонка у таблиці, котра теж назвивається Post 
    
class Category(models.Model):
    name = models.CharField(max_length=80)
    info = models.TextField(blank=True)
    category_slug = models.CharField(max_length=80, default="category_main")
    img = models.ImageField(upload_to='blog/static/img/categories',
                            height_field=None,
                            width_field=None,
                            verbose_name="Зображення категорії", 
                            default='default.jpg')
    class Meta:
        verbose_name_plural = "Категорії"
    def save(self,*agr, **kwargs):
        super().save()
        img = Image.open(self.img.path)
        if img.height>200 or img.width>200:
            img.thumbnail((200, 200))
            img.save(self.img.path)
    def __str__(self):
        return f"{self.name}   URL: {self.category_slug}"

class Post(models.Model): 
    title = models.CharField(max_length=100) #CharField - тип для короткого тексту
    text = models.TextField() #для зберігання тексту
    created_at = models.DateField(default=timezone.now) #час коли таблиця створена
    post_slug = models.CharField(max_length=80, default="default_post") #коротка назва поста для url
    img = models.ImageField(default = 'blog/static/img/default.jpeg', 
                            upload_to='blog/static/img', 
                            height_field=None, width_field=None,
                            max_length=200,
                            verbose_name="Картинка для поста") #поле для зображення
    category = models.ForeignKey(Category, default=1, 
                                 on_delete=models.SET_DEFAULT,
                                 verbose_name="Категорія")
    
    def __str__(self): #при викликанні print буде повертатися саме заголовок(title)
        return self.title
    def save(self,*agr, **kwargs):
        super().save()
        img = Image.open(self.img.path)
        if img.height>650 or img.width>650:
            img.thumbnail((650, 650))
            img.save(self.img.path)

    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(verbose_name="Уміст:")
    created_at = models.DateField(default=timezone.now)
    def __str__(self): 
        return self.content
