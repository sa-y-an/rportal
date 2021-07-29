from django.urls import path

from .views import (
    RegistrationView,
    AllUsersView,
    StudentRegistrationView,
    AllStudentsView,
    TeacherRegistrationView,
    AllTeachersView,
    RetrieveUpdateUserView,
    RetrieveUpdateStudentView,
    RetrieveUpdateTeacherView,
    resendVerificationView
)
from usr_val.views import activate
app_name = 'usr_val'

urlpatterns = [
    # user related
    path('register/', RegistrationView.as_view(), name='user_registration'),
    path('list/', AllUsersView.as_view(), name='all_users_list'),
    path('resend-user-activation/',resendVerificationView,name='resend-user-activation'),
    path('details/<str:username>/',RetrieveUpdateUserView.as_view(),name='user_update'),

    # student related
    path('student/create-profile/', StudentRegistrationView.as_view(), name='student_registration'),
    path('student/all/', AllStudentsView.as_view(), name='students'),
    path('student/details/<str:username>/', RetrieveUpdateStudentView.as_view(), name='student_update'),

    # teacher related
    path('teacher/create-profile/', TeacherRegistrationView.as_view(), name='teacher_registration'),
    path('teacher/all/', AllTeachersView.as_view(), name='teachers'),
    path('teacher/details/<str:username>/', RetrieveUpdateTeacherView.as_view(), name='teacher_update'),

    # Account Activation
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),

]
