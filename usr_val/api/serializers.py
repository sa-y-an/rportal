from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from usr_val.utils import institute_email_validator, LowerEmailField, FileValidator
from usr_val.models import Teacher, Student


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = LowerEmailField(
        required=True,
        allow_blank=False,
        label='Email address',
        max_length=30,
        validators=[UniqueValidator(queryset=User.objects.all()), institute_email_validator],
    )
    first_name = serializers.CharField(
        required=True,
        max_length=60,
        allow_blank=False
    )
    last_name = serializers.CharField(
        required=False,
        max_length=60,
        allow_blank=True,
        default=''
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'confirm_password': 'Passwords must match'})
        account = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'].lower(),
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            is_active=False  # TO BE CHANGED TO FALSE
        )
        account.set_password(password)
        account.save()
        # send email from here
        return account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups', 'id']


class StudentRegistrationSerializer(serializers.ModelSerializer):
    cv = serializers.FileField(allow_null=True,
                               max_length=100,
                               required=False,
                               use_url=True,
                               validators=[FileValidator(content_types=('application/pdf',), max_size=1024 * 1024)]
                               )

    class Meta:
        model = Student
        exclude = ['user', ]


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class TeacherRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        exclude = ['user', ]

    def save(self):
        try:
            request = self.context.get('request')
            user = request.user
        except Exception as e:
            raise serializers.ValidationError('Could not get the user')

        if user.groups.first().name != 'teacher':  # checks if the user is actually a teacher
            raise serializers.ValidationError('Student cannot create Teacher profile.')

        if Teacher.objects.filter(user=user).exists():
            raise serializers.ValidationError('Teacher profile already exists.')
        teacher = Teacher(
            user=user,
            branch=self.validated_data['branch'],
            contact=self.validated_data.get('contact'),
        )
        teacher.save()
        return teacher


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'
