from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    StudentRegistrationSerializer,
    StudentSerializer,
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


@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def studentRegistrationView(request):
    payload=request.data
    serializer=StudentRegistrationSerializer(data=payload or None)
    serializer.user=request.user
    data={}
    # print(serializer)
    if serializer.is_valid():
        account=serializer.save()
        status_code=status.HTTP_201_CREATED
        data['profile']=account

    else:
        data=serializer.errors
        status_code=status.HTTP_400_BAD_REQUEST

    return Response(data=data,status=status_code)


class AllUsersView(ListAPIView):
    queryset=User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class AllStudentsView(ListAPIView):
    queryset=Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAdminUser,)

