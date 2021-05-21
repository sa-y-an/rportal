from django.urls import path, include
from . import views


app_name = 'posts'

urlpatterns = [
    path('student/', views.studentd , name= 'studentd'),
    path('', views.feed, name = 'feed'),
    path('teacher/', views.teacherd, name='teacherd'),
]
