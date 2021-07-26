from django.contrib import admin
from .models import Post

from imagekit.admin import AdminThumbnail
# from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='avatar_thumbnail')


admin.site.register(Post, PhotoAdmin)


# Register your models here.
# admin.site.register(Post)