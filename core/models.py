from django.db import models
from userauth.models import User
from django.utils import timezone


class Post(models.Model):
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  title = models.CharField(max_length=100)
  content = models.TextField(max_length=200)
  image = models.ImageField(upload_to='images', null=True, blank=True)
  # likes = 
  is_hidden = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title[:50] 
    

class Comment(models.Model):
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
  content = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.content
