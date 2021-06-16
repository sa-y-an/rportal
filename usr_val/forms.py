from django.db.models import fields
from django.forms import ModelForm

from posts import models
import posts
from .models import Teacher
from django.contrib.auth.models import User
from django import forms
from posts.models import Post

class TeacherDetails(forms.Form):
    first_name = forms.CharField(max_length=400, label="Enter Your First Name") 
    last_name = forms.CharField(max_length=400, label="Enter Your Last Name")
    email = forms.EmailField(label='Please Enter Your Work Email')
    branch = forms.CharField(max_length=400, label="Enter Your college department")
    contact = forms.CharField(min_length=10, max_length=10, label="Enter your Phone Number", required=False)

class StudentDetails(forms.Form):
    first_name = forms.CharField(max_length=400, label="Enter Your First Name") 
    last_name = forms.CharField(max_length=400, label="Enter Your Last Name")
    email = forms.EmailField(label='Please Enter Your Work Email')
    branch = forms.CharField(max_length=400, label="Enter Your college department")
    contact = forms.CharField(min_length=10, max_length=10, label="Enter your Phone Number", required=False)

class PostCreationForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','image_url','tag','description']
        