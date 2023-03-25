from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import TemplateView, ListView, DetailView

from .forms import CreateCommentForm
from .models import Post

class MainView(ListView):
    model = Post
    template_name = 'core/index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = Post.objects.filter(Q(content__icontains=query)|
                                       Q(title__icontains=query)).order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = self.get_queryset()
        return context
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post-detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.all()
        context['comments'] = comments
        context['form'] = CreateCommentForm(post=post)
        return context
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CreateCommentForm(post=post, data=request.POST)
        if form.is_valid():
            form.instance.post = post
            form.save()
            return redirect('post-detail', pk=post.pk)
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
