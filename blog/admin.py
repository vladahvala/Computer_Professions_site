from django.contrib import admin
from .models import Post, Comment, Category
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'text', 'created_at', 'img', 'category', 'post_slug')

admin.site.site_header = "Адміністрування"
admin.site.site_title = "Адміністратор"

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)