from django.http.response import HttpResponseNotAllowed
from django.http import HttpResponse, HttpResponseNotFound
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
from .forms import PostCreationForm, TeacherDetails, StudentDetails
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post
from django.core.mail import send_mail


# teacher 

# Create your views here.
class SignupUser(View) :

    def get(self, request):
        return render(request, 'usr_val/signupuser.html', {'form':UserCreationForm()})


    def post(self,request):
        if request.POST['password1'] == request.POST['password2']:
            try:
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
            except IntegrityError:
                return render(request, 'usr_val/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
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
            return redirect('home:home')


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

        with open('text_messages/login_user.txt', 'r') as file:
            data_email = file.read()

        send_mail(
                'Signup Sucessfull',
                str(data_email).format(model.user.first_name , model.user.first_name , 
                model.user.last_name, model.contact , model.user.username ),
                'ieeesbnitd@gmail.com',
                [model.user.email],
                fail_silently=False,
                )
        
        return super().form_valid(form)




# student
class SignupStudent(View) :

    def get(self, request):
        return render(request, 'usr_val/signupstudent.html', {'form':UserCreationForm()})


    def post(self,request):
        if request.POST['password1'] == request.POST['password2']:
            try:
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
            except IntegrityError:
                return render(request, 'usr_val/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
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

        with open('text_messages/login_user.txt', 'r') as file:
            data_email = file.read()

        send_mail(
                'Signup Sucessfull',
                str(data_email).format(model.user.first_name , model.user.first_name , 
                model.user.last_name, model.contact , model.user.username ),
                'ieeesbnitd@gmail.com',
                [model.user.email],
                fail_silently=True,
                )
        
        return super().form_valid(form)






class TeacherPostCreation(LoginRequiredMixin, CreateView ):
    # model = Post
    form_class = PostCreationForm
    template_name = 'usr_val/teacherd.html'
    success_url = '/projects/'


    def form_valid(self,form):
        obj = form.save(commit = False)
        # print(obj)
        acessor = get_object_or_404(Teacher, user = self.request.user)
        obj.teacher = acessor
        obj.save()
        return super().form_valid(form)

        


def studentd(request):
    return render(request, 'usr_val/studentd.html')


@login_required
def apply(request, post_id):

    

    project = get_object_or_404(Post, pk = post_id)
    try :
        student = get_object_or_404(Student, user = request.user)
    except :
        student = None
    
    st_apply = False

    if request.method == 'GET':
        if student in project.student.all() :
            st_apply = True
        
        return render(request, 'usr_val/apply.html', {'i' : project , 'apply' :st_apply })


    if request.method == 'POST':

        if student == None :
            return HttpResponse("Only students can apply to a project")
        
        else : 

            message = 'please try later'

            if student not in project.student.all() :
                project.student.add(student)
                
                project.save()
                message = "You have Sucessfully Apllied to this project"

            else :
                message = "You have already apllied to this project"

            return render(request, 'usr_val/apply.html' , {'message' : message , 'i' : project})


    

@login_required
def info(request) :
    user = request.user
    teacher = get_object_or_404(Teacher, user = user)
    posts = Post.objects.filter(teacher = teacher)
    # print(posts.get(title = 'Matlab Mastery').student.all())
    # print(posts.student)
    return render(request, 'usr_val/info.html', {'posts' : posts})

@login_required
def stinfo(request, sid) :
    teacher = get_object_or_404(Teacher, user = request.user)
    project = get_object_or_404(Post, pk = sid)
    students = project.student.all()
    return render(request, 'usr_val/stinfo.html', {'students':students , 'project':project})

