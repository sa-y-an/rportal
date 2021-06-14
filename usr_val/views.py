from django.shortcuts import render
from django.views import View 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
class SignupUser(View) :

    def get(self, request):
        return render(request, 'usr_val/signupuser.html', {'form':UserCreationForm()})


    def post(self,request):
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home:home')
            except IntegrityError:
                return render(request, 'usr_val/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'usr_val/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})


class LoginUser(View):

    def get(self,request):
        pass

    def post(self,request):
        pass


class LogoutUser(View):

    def get(self,request):
        pass

    def post(self,request):
        pass

