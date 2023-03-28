# Generated by Django 4.1.3 on 2023-02-25 17:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='saving',
            field=models.ManyToManyField(blank=True, related_name='post_savings', to=settings.AUTH_USER_MODEL),
        ),
    ]