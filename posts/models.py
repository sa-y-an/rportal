from django.db import models
from usr_val.models import Teacher, Student

# Create your models here.
# static questions containing only text and images


class Post(models.Model):
    title = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True, default=' Will help your carrer')
    image_url = models.URLField(blank=True)
    tag = models.TextField(blank=True, default='open to all')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return self.title
