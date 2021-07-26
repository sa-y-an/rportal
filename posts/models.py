from django.db import models
from usr_val.models import Teacher, Student
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# used for image toolkit
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
# static questions containing only text and images


class Post(models.Model):

    class PostObjects(models.Manager):
        " Function to return only published models "
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')

    
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )


    title = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True, default=' Please provide a description ')
    details = models.FileField(null=True, 
                          upload_to='post/details',
                          validators=[FileExtensionValidator(allowed_extensions=['pdf', ])],
                          max_length=255
                          )
    tag = models.TextField(blank=True, default='open to all')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, blank=True)
    is_active = models.BooleanField(default=False)

    ## Image 

    avatar = models.ImageField(upload_to='avatars', default = 'default/project.png' )
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})




    ## Draft & Publish

    slug = models.SlugField(max_length=250, unique_for_date='published',blank= True)
    published = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10, choices=options, default='published')
    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    
