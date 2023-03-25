from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CustomUserCreationForm


class SignupView(CreateView):
    template_name = "userauth/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
    

class CustomLogoutView(LogoutView):
    next_page = 'index'
