from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  email = models.EmailField(unique=True, null=True)
  avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
  bio = models.TextField(null=True, blank=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  def get_full_name(self):
    # Combine the first and last name fields to get the user's full name
    return f"{self.first_name} {self.last_name}"
