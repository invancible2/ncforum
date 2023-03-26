from django.db import models
from userauth.models import User
from django.utils import timezone


class Post(models.Model):
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  title = models.CharField(max_length=100)
  content = models.TextField(max_length=200)
  image = models.ImageField(upload_to='images', null=True, blank=True)
  upvotes = models.PositiveIntegerField(default=0)
  downvotes = models.PositiveIntegerField(default=0)
  is_hidden = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  @property
  def score(self):
      return self.upvotes - self.downvotes

  def __str__(self):
    return self.title[:50] 
  

class Vote(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
  UPVOTE = 'U'
  DOWNVOTE = 'D'
  VOTE_CHOICES = [
      (UPVOTE, 'Upvote'),
      (DOWNVOTE, 'Downvote'),
  ]
  vote_type = models.CharField(
      max_length=1,
      choices=VOTE_CHOICES,
      default=UPVOTE,
  )


  class Meta:
      unique_together = ('user', 'post')

  def __str__(self):
      return f'{self.user} voted {self.value} on {self.post}'
    

class Comment(models.Model):
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
  content = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.content
