from usr_val.models import Teacher
from django.contrib import admin
from .models import Student, Teacher


# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)