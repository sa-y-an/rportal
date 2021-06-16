from django.shortcuts import render
from django.views import View 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Teacher,Student
from django.views.generic.edit import FormView, UpdateView, FormMixin
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import TeacherDetails, StudentDetails
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin



# teacher 

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
            return redirect('usr_val:teacher')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home:home')





class TeacherCreateView(LoginRequiredMixin,  FormView):
    template_name = 'usr_val/tdashboard.html'
    form_class = TeacherDetails
    success_url = '/'

    def form_valid(self, form):
        my_form = form.cleaned_data
        model = get_object_or_404(Teacher, user = self.request.user)
        model.user.first_name = my_form['first_name']
        model.user.last_name = my_form['last_name']
        model.user.email = my_form['email']
        model.user.save()

        model.branch = my_form['branch']
        model.contact = my_form['contact']
        model.save()
        
        return super().form_valid(form)




# student
class SignupStudent(View) :

    def get(self, request):
        return render(request, 'usr_val/signupstudent.html', {'form':UserCreationForm()})


    def post(self,request):
        if request.POST['password1'] == request.POST['password2']:
            # try:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            t = Student.objects.create(
            user=user)
            t.save()
            messages.success(request, 'Account was created for ' + user.username)                
            
            login(request, user)
            return redirect('home:home')
            # except IntegrityError:
            #     return render(request, 'usr_val/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'usr_val/signupstudent.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})



class StudentCreateView(LoginRequiredMixin,  FormView):
    template_name = 'usr_val/sdashboard.html'
    form_class = StudentDetails
    success_url = '/'

    def form_valid(self, form):
        my_form = form.cleaned_data
        model = get_object_or_404(Student, user = self.request.user)
        model.user.first_name = my_form['first_name']
        model.user.last_name = my_form['last_name']
        model.user.email = my_form['email']
        model.user.save()

        model.branch = my_form['branch']
        model.contact = my_form['contact']
        model.save()
        
        return super().form_valid(form)