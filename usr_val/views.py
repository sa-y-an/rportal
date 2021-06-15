from usr_val.forms import TeacherForm
from django.shortcuts import render
from django.views import View 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Teacher
from django.views.generic.edit import FormView
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import TeacherForm


# Create your views here.
class SignupUser(View) :

    def get(self, request):
        return render(request, 'usr_val/signupuser.html', {'form':UserCreationForm()})


    def post(self,request):
        if request.POST['password1'] == request.POST['password2']:
            # try:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            group = Group.objects.get(name='teacher')
            user.groups.add(group)
            t = Teacher.objects.create(
            user=user)
            t.save()
            messages.success(request, 'Account was created for ' + user.username)                
            
            login(request, user)
            return redirect('home:home')
            # except IntegrityError:
            #     return render(request, 'usr_val/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'usr_val/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})


class LoginUser(View):

    def get(self,request):
        return render(request, 'usr_val/loginuser.html', {'form':AuthenticationForm()})

    def post(self,request):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'usr_val/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('usr_val:tdashboard')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home:home')





class TeacherFormView(FormView):
    template_name = 'usr_val/tadasboard.html'
    form_class = TeacherForm
    success_url = ''

    def form_valid(self, form):
        form.instance = self.request.user
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)