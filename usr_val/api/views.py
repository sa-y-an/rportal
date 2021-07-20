from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
from rest_framework.serializers import ValidationError
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    StudentRegistrationSerializer,
    StudentSerializer,
    TeacherRegistrationSerializer,
    TeacherSerializer,
)
from usr_val.models import Student, Teacher
from usr_val.utils import sendVerificationEmail
from django.contrib.sites.shortcuts import get_current_site


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        current_site = get_current_site(self.request)
        msg = sendVerificationEmail(domain=current_site.domain, user=user)
        print(msg)


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


@api_view(['POST', ])
@throttle_classes([AnonRateThrottle, ])
def resendVerificationView(request):
    data = request.data
    email = data.get('email')
    if email is None:
        raise ValidationError('Email must be provided.')
    response = {'msg': 'If the provided email exists, then the verification email is being sent.'}
    inactive_users = User.objects.filter(is_active=False)
    users = inactive_users.filter(email=email)
    if not users.exists():
        return Response(data={'msg': "You either have activated account or you haven't created account yet"})
    domain = get_current_site(request).domain

    msg = sendVerificationEmail(domain=domain, user=users.first())
    print(msg)
    return Response(data=response)
