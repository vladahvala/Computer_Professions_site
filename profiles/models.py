import uuid 
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    username = models.CharField(max_length=200)
    profession = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='img', blank=True, null=True, default='profile/default_user_img.jpg')
    about = models.TextField(max_length=205)

    profile_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.username
