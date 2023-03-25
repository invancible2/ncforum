from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('auth/', include('userauth.urls')),
]
