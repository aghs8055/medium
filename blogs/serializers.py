from rest_framework import serializers

from blogs.models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['owner']
        extra_kwargs = {
            'views': {'read_only': True},
            'likes': {'read_only': True}
        }