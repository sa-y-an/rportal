from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'usr_val'

urlpatterns = [
    
    # Auth
    path('signupuser/', views.SignupUser.as_view() , name="signupuser"),
    path('signupstudent/', views.SignupStudent.as_view() , name="signupstudent"),

    path('loginuser/', views.LoginUser.as_view() , name="loginuser"),
    path('logout/', views.logoutuser, name='logoutuser'),
    

    # Teacher

    path('teacher/',views.TeacherCreateView.as_view() , name='teacher'),
    path('student/',views.StudentCreateView.as_view() , name='student'),


    # post creation 
    path('teacherd/', views.TeacherPostCreation.as_view(), name='teacherd'),
    path('student', views.studentd, name='studentd'),

    # individual posts
    path('project/<int:post_id>/', views.apply, name='apply'),

    #info
    path('info', views.info , name= 'info' ),
    path('stinfo/<int:sid>', views.stinfo , name= 'stinfo' ),


    # email reset 

]