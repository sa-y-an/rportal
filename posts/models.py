from django.db import models


# Create your models here.

# static questions containing only text and images


class Post(models.Model):
    title = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True, default='hello')
    image_url = models.URLField(blank=True)
    tag = models.TextField(blank=True, default='hint')

    def __str__(self):
        return self.title
