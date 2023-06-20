from rest_framework.response import Response
from rest_framework import generics


from .serializers import PostSerializer
from ..models import Post


class PostsListAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostsCreateRetrieve(mixins.CreateMixin)