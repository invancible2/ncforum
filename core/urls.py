from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('create/', views.CreatePostView.as_view(), name='create-post'),
    path('<int:pk>/edit/', views.EditPostView.as_view(), name='edit-post'),
    path('<int:pk>/delete/', views.DeletePostView.as_view(), name='delete-post'),
    path('<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('auth/', include('userauth.urls')),

    path('vote/<int:post_id>/', views.vote, name='vote'),
]
