from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, throttle_classes
from django.db.models import Sum

from blogs.serializers import BlogSerializer
from blogs.serializers import Blog
from blogs.throttles import IPRateThrottle


class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):    
        return Response(BlogSerializer(Blog.objects.all(), many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        blog = Blog.objects.filter(pk=pk).first()
        if not blog:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        if blog.owner != request.user:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = BlogSerializer(instance=blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        blog = Blog.objects.filter(pk=pk).first()
        if not blog:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        if blog.owner != request.user:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        
        blog.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET'])
@throttle_classes([IPRateThrottle])
def detail_blog(request, pk):
    blog = Blog.objects.filter(pk=pk).first()
    if not blog:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    
    blog.views += 1
    blog.save()
    
    return Response(BlogSerializer(blog).data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def like_blog(request, pk):
    blog = Blog.objects.filter(pk=pk).first()
    if not blog:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    
    if not request.user.is_authenticated:
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    
    blog.likes += 1
    blog.save()
    
    return Response(BlogSerializer(blog).data, status=status.HTTP_200_OK)

    
@api_view(['POST'])
def analytics(request):
    if not request.user.is_authenticated:
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(
        Blog.objects.filter(owner=request.user).aggregate(total_views=Sum('views'), total_likes=Sum('likes')),
        status=status.HTTP_200_OK,
    )