from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('auth/', include('userauth.urls')),
]
