from django.shortcuts import render
from django.db.models import Q
from django.views.generic import TemplateView, ListView

from .models import Post

class MainView(ListView):
    model = Post
    template_name = 'core/index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = Post.objects.filter(Q(content__icontains=query)).order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = self.get_queryset()
        return context