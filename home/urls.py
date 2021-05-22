from django.urls import path, include
from . import views


app_name = 'home'

urlpatterns = [
    path('', views.home , name= 'home'),
    path('about/', views.about , name= 'about'),
    path('director/', views.director , name= 'director'),
    path('mile/', views.mile , name= 'mile'),
    path('team/', views.team , name= 'team'),
]
