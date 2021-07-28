from rest_framework import serializers
from usr_val.utils import FileValidator
from usr_val.api.serializers import TeacherSerializer, StudentSerializer

from .models import Post, SOP


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model=Post
        exclude=('is_active', 'published','student')

class PostPublishedSerializer(serializers.ModelSerializer):

    avatar_thumbnail = serializers.ImageField(read_only=True)
    teacher = TeacherSerializer()

    class Meta:
        fields = ( 'title', 'description', 'tag', 'teacher', 'published', 'avatar_thumbnail','slug')
        
        model = Post


class CreatePostSerializer(serializers.ModelSerializer):
    details = serializers.FileField(
        allow_null=True,
        max_length=100,
        required=False,
        use_url=True,
        validators=[FileValidator(content_types=('application/pdf',), max_size=10*1024 * 1024)],
                                   )

    class Meta:
        model=Post
        read_only_fields=('slug', )
        fields = ('title','description', 'details','tag', 'is_active','status', 'slug')


class RetrieveUpdatePostSerializer(serializers.ModelSerializer):
    teacher=TeacherSerializer()
    applied=serializers.SerializerMethodField(method_name='get_applied')

    class Meta:
        model=Post
        exclude=('is_active', 'published','student')
        read_only_fields=('slug', )

    def get_applied(self,obj,*args,**kwargs):
        """:returns -1 if teacher, 0 if not applied, 1 if applied"""
        req=self.context.get('request',{})
        user=req.user
        if user.groups.first().name!='student':
            return -1

        return 1 if obj.student.filter(applied_students__student__user=user).exists() else 0


class SOPSerializer(serializers.ModelSerializer):
    document = serializers.FileField(
        allow_null=False,
        max_length=100,
        required=True,
        use_url=True,
        validators=[FileValidator(content_types=('application/pdf',), max_size=15 * 1024 * 1024)],
    )
    student=StudentSerializer(read_only=True)
    post=PostSerializer(read_only=True)

    class Meta:
        model= SOP
        fields = '__all__'
        read_only_fields=('student', 'post')


class AcceptanceSerializer(serializers.ModelSerializer):
    stud_username=serializers.CharField(max_length=128)
    accepted=serializers.ChoiceField(choices=[(0, 'Applied'), (-1, 'Rejected'), (1, 'Accepted')], required=True)

    class Meta:
        model=SOP
        fields=('accepted','stud_username')

