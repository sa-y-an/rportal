from django.shortcuts import render
from .models import Post

# Create your views here.

def feed(request):
    posts = Post.objects.all()
    return render(request, "posts/feed.html", {'posts': posts})

