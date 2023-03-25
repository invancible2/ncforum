from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
