from django.shortcuts import render
from .models import Post

# Create your views here.
def studentd(request):
    return render(request, 'posts/studentd.html')

def teacherd(request):
    return render(request, 'posts/teacherd.html')

def feed(request):
    posts = Post.objects.all()
    return render(request, "posts/feed.html", {'posts': posts})