from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
from rest_framework.serializers import ValidationError
from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    StudentRegistrationSerializer,
    StudentSerializer,
    TeacherRegistrationSerializer,
    TeacherSerializer,
)
from usr_val.models import Student, Teacher
from usr_val.utils import account_activation_token, ThreadedMailing
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def perform_create(self,serializer):
        user=serializer.save()
        current_site = get_current_site(self.request)

        mail_subject = 'Activate your IEEE Research Portal account.'
        message = render_to_string('usr_val/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': account_activation_token.make_token(user),
        })
        to_email=serializer.validated_data['email']
        mail=EmailMessage(
            mail_subject,
            message,
            to=[to_email,]
        )
        threaded_mail=ThreadedMailing(mail)
        threaded_mail.start()


class StudentRegistrationView(CreateAPIView):
    serializer_class = StudentRegistrationSerializer

    def get_serializer_context(self):
        context = super(StudentRegistrationView, self).get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def perform_create(self,serializer):
        try:
            user = self.request.user
        except Exception as e:
            raise ValidationError('Could not get user')

        if user.groups.first().name != 'student':  # checks if the user is actually a student
            raise ValidationError('Teacher cannot create Student profile.')

        if Student.objects.filter(user=user).exists():
            raise ValidationError('Profile already exists.')

        serializer.save(user=self.request.user)


class TeacherRegistrationView(CreateAPIView):
    serializer_class = TeacherRegistrationSerializer

    def get_serializer_context(self):
        context = super(TeacherRegistrationView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class AllUsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class AllStudentsView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAdminUser,)


class AllTeachersView(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (IsAdminUser,)
