from django.urls import path
from . import views

from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'posts'

urlpatterns = [
    path('', views.PostPublishedList.as_view(), name='feed'),
    path('details/<slug:slug>/', views.ProjectRetrieveUpdateView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('apply/<slug:slug>/', views.apply_project, name='apply_post'),
    path('shortlist/<slug:slug>/', views.shortlistStudents, name='shortlist'),
    path('applied/<slug:slug>/', views.AppliedStudentsView.as_view(), name='applied_students'),
    path('withdraw/<slug:slug>/', views.withdrawApplicationView, name='withdraw_application'),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
