from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def director(request):
    return render(request, 'home/director.html')

def mile(request):
    return render(request, 'home/mile.html')

def team(request):
    return render(request, 'home/team.html')