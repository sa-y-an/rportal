from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator
from .constants import (
    DEPARTMENTS,
)
from .utils import get_group_name


def cv_upload_location(instance, filename, **kwargs):
    file_path = 'CVS/{username}.pdf'.format(username=instance.user.username)
    return file_path


# Create your models here.


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=4, choices=DEPARTMENTS)
    contact = models.CharField(blank=True, max_length=15)

    def __str__(self):
        return self.user.username

    def get_group_name(self):
        return self.user.groups.first()

    class Meta:
        ordering = ('id',)


class Student(models.Model):
    dp = models.FileField(blank=True,
                          null=True,
                          upload_to="students/dp",
                          validators=[FileExtensionValidator(allowed_extensions=['png', '.jpg', '.jpeg', ], )],
                          max_length=255
                          )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=4, choices=DEPARTMENTS)
    contact = models.CharField(blank=True, null=True, max_length=15)
    cgpa = models.FloatField(default=00.00)
    cv = models.FileField(null=True,
                          upload_to=cv_upload_location,
                          validators=[FileExtensionValidator(allowed_extensions=['pdf', ])],
                          max_length=255
                          )

    sop = models.TextField(default=" Please write what inspires you. ", max_length=1000)

    def __str__(self):
        return self.user.username

    def get_group_name(self):
        return self.user.groups.first()

    class Meta:
        ordering = ('id',)


def post_save_userGroup(sender, instance, *args, **kwargs):
    if not instance.groups.exists():
        if instance.is_superuser:
            group_name = 'teacher'
        else:
            group_name = get_group_name(instance.email)
        group, created = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)


post_save.connect(post_save_userGroup, sender=User)
