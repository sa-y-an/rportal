from django.contrib import admin
from .models import Student, Teacher, ResearchStatement

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(ResearchStatement)
