from django.urls import path, include
from . import views
from rest_framework.schemas import get_schema_view

app_name = 'home'

urlpatterns = [
    path('', views.home , name= 'home'),
    path('about/', views.about , name= 'about'),
    path('director/', views.director , name= 'director'),
    path('mile/', views.mile , name= 'mile'),
    path('team/', views.team , name= 'team'),

    ## Api Documentation 

    path('schema', get_schema_view(
        title="RpBackendAPI",
        description="API for the Research Portal",
        version="1.0.0"
    ), name='openapi-schema'),


]
