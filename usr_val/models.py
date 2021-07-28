from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator
from .constants import (
    DEPARTMENTS,
)
from .utils import get_group_name
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


def cv_upload_location(instance, filename, **kwargs):
    file_path = 'CVS/{username}.pdf'.format(username=instance.user.username)
    return file_path


# Create your models here.


class Teacher(models.Model):

    avatar = models.ImageField(upload_to='avatars', default = 'default/einstein.jpg' )
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=4, choices=DEPARTMENTS, blank= True)
    contact = models.CharField(blank=True, max_length=15)

    def __str__(self):
        return self.user.username

    def get_group_name(self):
        return self.user.groups.first()

    class Meta:
        ordering = ('id',)


class Student(models.Model):

    avatar = models.ImageField(upload_to='avatars', default = 'default/einstein.jpg' )
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=4, choices=DEPARTMENTS, blank= True)
    contact = models.CharField(blank=True, null=True, max_length=15)
    cgpa = models.FloatField(default=00.00)
    cv = models.FileField(null=True,
                            blank=True,
                          upload_to=cv_upload_location,
                          validators=[FileExtensionValidator(allowed_extensions=['pdf', ])],
                          max_length=255
                          )
    curr_project=models.ForeignKey('posts.Post',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL,
                                   related_name='current_project',
                                   )

    def __str__(self):
        return self.user.username

    def get_group_name(self):
        return self.user.groups.first()

    class Meta:
        ordering = ('id',)




class ResearchStatement(models.Model) :
    " a one to one model with Student  this allows drafting the statement before Submitting "

    class PostObjects(models.Manager):
        " Function to return only published models "
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')

    
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    research_statement = models.TextField(default=" Please write what inspires you to do Research ", max_length=1000)
    student = models.ForeignKey(Student, on_delete= models.CASCADE)

    status = models.CharField(
        max_length=10, choices=options, default='published')
    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager


    def __str__(self):
        return self.user.username









def post_save_userGroup(sender, instance, *args, **kwargs):
    if not instance.groups.exists():
        if instance.is_superuser:
            group_name = 'teacher'
        else:
            group_name = get_group_name(instance.email)
        group, created = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)


post_save.connect(post_save_userGroup, sender=User)
