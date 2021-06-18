from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
# import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('projects/', include('posts.urls')),
    path('users/', include('usr_val.urls')),


    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="usr_val/password_reset.html"),
    name="reset_password"),

    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name="usr_val/password_reset_sent.html"), 
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="usr_val/password_reset_form.html"), 
    name="password_reset_confirm"),

    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name="usr_val/password_reset_done.html"), 
    name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)