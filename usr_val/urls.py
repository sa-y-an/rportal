from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'usr_val'

urlpatterns = [
    
    # Auth
    path('signupuser/', views.SignupUser.as_view() , name="signupuser"),
    path('loginuser/', views.LoginUser.as_view() , name="loginuser"),
    path('logout/', views.logoutuser, name='logoutuser'),
    

    # Teacher

    path('teacher/',views.TeacherFormView , name='teacher')
]