from django import forms

from .models import Post, Comment


class CreatePostForm(forms.ModelForm):
  image = forms.ImageField(required=False)
  class Meta:
    model = Post
    fields = ['content', 'image']


class CreateCommentForm(forms.ModelForm):
  content = forms.CharField(widget=forms.Textarea(
    attrs={
        'rows': 5
    }
  ))

  def __init__(self, post, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.post = post
      
  class Meta:
    model = Comment
    fields = ('content',)