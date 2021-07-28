from django.shortcuts import render
from django.http import Http404
from django.views import generic
from .models import Post, SOP
from .serializers import (
    PostSerializer,
    PostPublishedSerializer,
    CreatePostSerializer,
    RetrieveUpdatePostSerializer,
    SOPSerializer,
    AcceptanceSerializer,
)

from rest_framework import generics
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from usr_val.models import Teacher, Student
from usr_val.api.serializers import StudentSerializer


class PostPublishedList(generics.ListAPIView):
    " Returns Only Published Posts "
    queryset = Post.postobjects.all()
    serializer_class = PostPublishedSerializer



class PostList(APIView):
    'List all posts or create a new post'

    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        posts=Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostDetail(APIView):
    'Read, update or delete an individual post'

    permission_classes=[permissions.IsAuthenticatedOrReadOnly]


    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        post=self.get_post(pk)
        serializer=PostSerializer(post)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        post=self.get_post(pk)
        serializer=PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post=self.get_post(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCreateView(generics.CreateAPIView):
    serializer_class = CreatePostSerializer

    def perform_create(self, serializer):
        try:
            user = self.request.user
        except Exception as e:
            raise ValidationError('Could not get user!')

        if user.groups.first().name != 'teacher':  # checks if the user is actually a teacher
            raise ValidationError('Student cannot create Projects.')
        profile = Teacher.objects.filter(user=user)
        if not profile.exists():
            raise ValidationError('The profile must be filled up before posting project.')
        profile=profile.first()
        serializer.save(teacher=profile)


class ProjectRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = RetrieveUpdatePostSerializer
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super(ProjectRetrieveUpdateView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def check_update_permissions(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()
        if user.groups.first().name!='teacher':
            raise ValidationError('Only teachers can modify projects!')
        if not user == obj.teacher.user:
            raise ValidationError("Can not change someone else's Project!")
        return True

    def check_view_permission(self,request,*args,**kwargs):
        obj=self.get_object()
        user = request.user
        if (obj.status=='draft' or obj.is_active==False) and obj.teacher.user!=user:
            raise ValidationError('Requested project not available!')
        return True

    def put(self, request, *args, **kwargs):
        _ = self.check_update_permissions(request, *args, **kwargs)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        _ = self.check_update_permissions(request, *args, **kwargs)
        return self.partial_update(request, *args, **kwargs)

    def get(self,request,*args,**kwargs):
        _=self.check_view_permission(request, *args, **kwargs)
        return self.retrieve(request, *args,**kwargs)


@api_view(['POST', ])
@permission_classes([IsAuthenticated,])
def apply_project(request, *args,**kwargs):
    project=Post.postobjects.filter(slug=kwargs.get('slug', ''))
    if project.exists():
        project=project.first()
    else:
        raise ValidationError('Requested project DNE')

    user = request.user
    data={}
    if user.groups.first().name!='student':
        raise ValidationError('Only studs can apply for projects')

    profile=Student.objects.filter(user=user)
    if (not profile.exists()) or (not profile.first().cv):
        raise ValidationError('Must upload CV before applying')
    profile=profile.first()
    if SOP.objects.filter(student=profile,post=project).exists():
        raise ValidationError('Already applied(SOP is filled up)!')
    if project.student.filter(applied_students__student=profile).exists():
        raise ValidationError('You have already applied')
    serializer=SOPSerializer(data=request.data)
    if serializer.is_valid():
        sop=serializer.save(post=project, student=profile)
        project.student.add(profile)
        data['sop']=serializer.data
    else:
        data=serializer.errors

    return Response(data=data)


@api_view(['POST', ])
@permission_classes([IsAuthenticated,])
def shortlistStudents(request,slug,*args,**kwargs):
    user=request.user
    qs=Post.objects.filter(teacher__user=user)
    project=generics.get_object_or_404(qs,**{'slug':slug})
    ser=AcceptanceSerializer(data=request.data)
    _= ser.is_valid(raise_exception=True)
    stud=Student.objects.filter(user__username=ser.validated_data['stud_username'])
    verdict=ser.validated_data['accepted']
    if (verdict is None) or (not stud.exists()):
        raise ValidationError('Please provide proper username(of student) and proper verdict')
    stud=stud.first()
    sop=SOP.objects.filter(post=project,student=stud)
    if not sop.exists():
        raise ValidationError('No SOP exists for the student in this project!')
    sop=sop.first()
    sop.accepted=verdict
    sop.save()
    return Response(data=SOPSerializer(instance=sop).data)


class AppliedStudentsView(generics.ListAPIView):
    serializer_class = StudentSerializer
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        slug=self.kwargs.get(self.lookup_url_kwarg)
        user=self.request.user
        # print(slug)
        qs=Post.postobjects.all()
        proj=generics.get_object_or_404(qs,**{'slug':slug,'teacher__user':user})
        studs=Student.objects.filter(sop__post=proj,sop__accepted=0)
        return studs




