from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=120)
    password1 = models.CharField(max_length=120)
    contact_number = PhoneNumberField(null=False, blank=False, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

class Post(models.Model):
    post_img = models.ImageField(upload_to='post_imgs/', null=True, blank=True)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=100000)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=datetime.now)
    