from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Teacher(models.Model):

    branch = models.CharField(blank=True, max_length=200)
    contact = models.CharField(blank=True,max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username

#student
class Student(models.Model):

    branch = models.CharField(blank=True, max_length=200)
    contact = models.CharField(blank=True,max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username