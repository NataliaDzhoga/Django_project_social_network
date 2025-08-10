from django.shortcuts import render

# Create your views here.


from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, PostCommSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            serializer = PostCommSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            raise NotFound('Ошибка 404')

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound('Ошибка 404')

        serializer = CommentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound('Ошибка 404')

        serializer = LikeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
