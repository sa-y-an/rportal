from django.db import models
from django.db.models.base import Model
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save

# used for image toolkit
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

import datetime

from usr_val.models import Teacher, Student


# Create your models here.
# static questions containing only text and images


class Post(models.Model):
    class PostObjects(models.Manager):
        """ Function to return only published models """

        def get_queryset(self):
            return super().get_queryset().filter(status='published', is_active=True)

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True, default=' Please provide a description ')
    details = models.FileField(null=True,
                               blank=True,
                               upload_to='post/details',
                               validators=[FileExtensionValidator(allowed_extensions=['pdf', ])],
                               max_length=255
                               )
    tag = models.TextField(blank=True, default='open to all')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, blank=True, related_name="applied_students")
    is_active = models.BooleanField(default=False)

    # Image

    avatar = models.ImageField(upload_to='avatars', default='default/project.png')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})

    # Draft & Publish

    slug = models.SlugField(max_length=250)
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=options, default='published')
    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title


# SOP Model


def sop_upload_location(instance, filename, **kwargs):
    file_path = 'SOP/{username}/{filename}.pdf'.format(username=instance.student.user.username, filename=filename)
    return file_path


class SOP(models.Model):
    """ Every student would be able to submit different SOP for each project """

    document = models.FileField(null=True,
                                blank=True,
                                upload_to=sop_upload_location,
                                validators=[FileExtensionValidator(allowed_extensions=['pdf', ])],
                                max_length=255
                                )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    accepted = models.SmallIntegerField(
        default=0,
        choices=[
            (0, 'Applied'),
            (-1, 'Rejected'),
            (1, 'Accepted')
        ]
    )  # 0 means applied(NA), -1 is Rejected, 1 is Accepted

    def __str__(self):
        return self.student.user.username

    class Meta:
        unique_together = ('student', 'post')


@receiver(pre_save, sender=Post)
def pre_save_blog_post(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(
            instance.teacher.user.username + '-' + instance.title + '-' + datetime.datetime.now().strftime("%Y%H%M%S%f")
        )
