from django.db import models
from django.utils import timezone
from PIL import Image 
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile

class Category(models.Model):
    name = models.CharField(max_length=80)
    info = models.TextField(blank=True)
    category_slug = models.CharField(max_length=80, default="category_main")
    img = models.ImageField(upload_to='images/',
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
        return f"{self.name}"
        # return f"{self.name}   URL: {self.category_slug}"

from django.urls import reverse

class Post(models.Model): 
    writer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100) 
    text = models.TextField()
    created_at = models.DateField(default=timezone.now) 
    post_slug = models.CharField(max_length=80, default="default_post") 
    img = models.ImageField(default='images/default.jpg', upload_to='images/', 
                            height_field=None, width_field=None,
                            max_length=200,
                            verbose_name="Картинка для поста")
    category = models.ForeignKey(Category, default=1, 
                                 on_delete=models.SET_DEFAULT,
                                 verbose_name="Категорія")

    def __str__(self): 
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.img.path)
        if img.height > 650 or img.width > 650:
            img.thumbnail((650, 650))
            img.save(self.img.path)

    def get_absolute_url(self):
        return reverse('post_url', args=[self.post_slug])
