from django.shortcuts import render

# Create your views here.
def studentd(request):
    return render(request, 'posts/studentd.html')

def teacherd(request):
    return render(request, 'posts/teacherd.html')

def feed(request):
    return render(request, 'posts/feed.html')