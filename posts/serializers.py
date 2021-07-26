from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model=Post
        fields= '__all__'

class PostPublishedSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ( 'title', 'description', 'tag', 'teacher', 'student', 'published')
        model = Post