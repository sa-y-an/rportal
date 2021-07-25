from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.serializers import ValidationError
from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    StudentRegistrationSerializer,
    StudentSerializer,
    TeacherRegistrationSerializer,
    TeacherSerializer,
    RetrieveUpdateUserSerializer,
    RetrieveUpdateStudentSerializer,
    RetrieveUpdateTeacherSerializer,
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
        # print(msg)


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


class BaseRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'username'

    def check_update_permissions(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()
        if not user == obj:
            raise ValidationError("Can not change someone else's account!")
        return True

    def put(self, request, *args, **kwargs):
        _ = self.check_update_permissions(request, *args, **kwargs)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        _ = self.check_update_permissions(request, *args, **kwargs)
        return self.partial_update(request, *args, **kwargs)


class RetrieveUpdateUserView(BaseRetrieveUpdateView):
    queryset = User.objects.all()
    serializer_class = RetrieveUpdateUserSerializer
    lookup_field = 'username'

    def check_update_permissions(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()
        if not user == obj:
            raise ValidationError("Can not change someone else's account!")
        return True


class RetrieveUpdateStudentView(BaseRetrieveUpdateView):
    queryset = Student.objects.all()
    serializer_class = RetrieveUpdateStudentSerializer
    lookup_field = 'user__username'

    def check_update_permissions(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()
        if not user == obj.user:
            raise ValidationError("Can not change someone else's Student account!")
        return True


class RetrieveUpdateTeacherView(BaseRetrieveUpdateView):
    queryset = Teacher.objects.all()
    serializer_class = RetrieveUpdateTeacherSerializer
    lookup_field = 'user__username'

    def check_update_permissions(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()
        if not user == obj.user:
            raise ValidationError("Can not change someone else's Faculty account!")
        return True


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
    # print(msg)
    return Response(data=response)
