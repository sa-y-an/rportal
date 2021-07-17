from django.urls import path

from .views import (
    RegistrationView,
    AllUsersView,
    StudentRegistrationView,
    AllStudentsView,
    TeacherRegistrationView,
    AllTeachersView,
)

app_name = 'usr_val'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='user_registration'),
    path('list/', AllUsersView.as_view(), name='all_users_list'),
    path('student/create-profile/', StudentRegistrationView.as_view(), name='student_registration'),
    path('student/all/', AllStudentsView.as_view(), name='students'),
    path('teacher/create-profile/', TeacherRegistrationView.as_view(), name='teacher_registration'),
    path('teacher/all/', AllTeachersView.as_view(), name='teachers'),
]
