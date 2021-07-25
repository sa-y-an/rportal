from copy import error
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Post
from .serializers import PostSerializer
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

def feed(request):
    posts = Post.objects.all()
    return render(request, "posts/feed.html", {'posts': posts})

class PostView(APIView):
    def get_post(self,pk):
        return Post.objects.get(pk=pk)

    def patch(self, request, pk):
        post=self.get_post(pk)
        serializer=PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        post=self.get_post(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
