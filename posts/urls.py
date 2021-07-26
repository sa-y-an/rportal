from django.urls import path
from . import views

from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name = 'feed'),
    path('allposts', views.PostList.as_view(), name='post_list'),
    path('<int:pk>', views.PostDetail.as_view(), name='post_detail')
]

urlpatterns =format_suffix_patterns(urlpatterns)
