from django.shortcuts import render, redirect
from .models import Post
from follow.models import Follow
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    # grab the post with true featured
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_follow = Follow()
        new_follow.email = email
        new_follow.save()

    context = {
        'object_list': featured,
        'latest': latest
    }
    return render(request, 'index.html', context)

def blog(request):
    return render(request, 'blog.html', {})

def post(request):
    return render(request, 'post.html', {})
