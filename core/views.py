from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView

from .forms import CreateCommentForm, CreatePostForm
from .models import Post, Vote
from userauth.models import User

class MainView(ListView):
    model = Post
    template_name = 'core/index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = Post.objects.filter(
                    Q(is_hidden=False) &
                    (Q(content__icontains=query) | Q(title__icontains=query))
                    ).order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = self.get_queryset()
        # context['scores'] = [post.score for post in context['posts']]
        return context
    

def vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    print('REACH')
    
    if user.is_authenticated:
        # Check if the user has already voted on this post
        try:
            vote = Vote.objects.get(user=user, post=post)
            if vote.vote_type == request.POST['vote_type']:
                # User is trying to upvote or downvote the same post again
                # if vote.vote_type == Vote.UPVOTE:
                #     post.upvotes -= 1
                # else:
                #     post.downvotes -= 1
                # vote.delete()
                return redirect('index')
            else:
                # User is changing their vote from upvote to downvote or vice versa
                if vote.vote_type == Vote.UPVOTE:
                    post.upvotes -= 1
                    post.downvotes += 1
                else:
                    post.upvotes += 1
                    post.downvotes -= 1
                vote.vote_type = request.POST['vote_type']
                vote.save()
                post.save()
                return redirect('index')
        except Vote.DoesNotExist:
            # User has not yet voted on this post
            vote = Vote(user=user, post=post, vote_type=request.POST['vote_type'])
            if vote.vote_type == Vote.UPVOTE:
                post.upvotes += 1
            else:
                post.downvotes += 1
            vote.save()
            post.save()
            return redirect('index')
    else:
        return redirect('login')


class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post-detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # context['scores'] = [post.score for post in context['posts']]
        comments = post.comments.all()
        context['comments'] = comments
        context['form'] = CreateCommentForm(post=post)
        return context
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CreateCommentForm(post=post, data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
        

class CreatePostView(View):
    form_class = CreatePostForm
    template_name = 'core/create-post.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            image = request.FILES.get('image')
            if image:
                post.image = image
            post.save()

            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'core/update-post.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404
        return obj
    

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'core/delete-post.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Set the is_hidden attribute to True instead of actually deleting the post
        self.object.is_hidden = True
        self.object.save()
        return redirect(self.success_url)

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'core/profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        user_id = self.kwargs['pk']
        return User.objects.get(id=user_id)
