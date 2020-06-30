from django import forms
from .models import Post, Comment
from tinymce import TinyMCE

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, initial):
        return False

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(attrs={
            'required': False,
            'cols': 30,
            'rows': 10
        }))

    class Meta:
        model = Post
        fields = '__all__'

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': "usercomment",
        'rows': '4',
    }))
    class Meta:
        model = Comment
        fields = ('content',)  # only need the content field in Comment in models.py