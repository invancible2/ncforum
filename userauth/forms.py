from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
  avatar = forms.ImageField(required=False)
  bio = forms.CharField(max_length=500, required=False)

  class Meta(UserCreationForm.Meta):
    model = User
    fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)