from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    StudentRegistrationSerializer,
    StudentSerializer,
    TeacherRegistrationSerializer,
    TeacherSerializer,
)
from usr_val.models import Student, Teacher


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer


class StudentRegistrationView(CreateAPIView):
    serializer_class = StudentRegistrationSerializer

    def get_serializer_context(self):
        context = super(StudentRegistrationView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


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
