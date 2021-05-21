from django.contrib import admin
from django.urls import path, include
import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'))
]
