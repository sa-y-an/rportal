from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model=Post
        fields= '__all__'

class PostPublishedSerializer(serializers.ModelSerializer):

    avatar_thumbnail = serializers.ImageField(read_only=True)


    class Meta:
        fields = ( 'title', 'description', 'tag', 'teacher', 'published', 'avatar_thumbnail')
        
        model = Post