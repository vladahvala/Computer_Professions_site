from django.contrib import admin
from tinymce.widgets import TinyMCE
from .models import Post, Comment, Category
from django.db import models
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'text', 'created_at', 'img', 'category', 'post_slug')
    formfield_overrides = { models.TextField: {'widget': TinyMCE}}

admin.site.site_header = "Адміністрування"
admin.site.site_title = "Адміністратор"

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)