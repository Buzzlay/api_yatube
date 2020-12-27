from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return self.queryset

    def partial_update(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post,
            id=self.kwargs['pk']
        )
        if self.request.user != post.author:
            return Response(
                request.data,
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.serializer_class(
            post,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.errors,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post,
            id=self.kwargs['pk']
        )
        if self.request.user != post.author:
            return Response(
                request.data,
                status=status.HTTP_403_FORBIDDEN
            )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            id=self.kwargs['post_id']
        )
        serializer.save(
            author=self.request.user,
            post=post,
        )

    def get_queryset(self):
        post = get_object_or_404(
            Post,
            id=self.kwargs['post_id']
        )
        return post.comments.all()

    def partial_update(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post,
            id=self.kwargs['post_id']
        )
        comment = get_object_or_404(
            Comment,
            post=post,
            id=self.kwargs['pk']
        )
        if self.request.user != comment.author:
            return Response(
                request.data,
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.serializer_class(
            comment,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.errors,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post,
            id=self.kwargs['post_id']
        )
        comment = get_object_or_404(
            Comment,
            post=post,
            id=self.kwargs['pk']
        )
        if self.request.user != comment.author:
            return Response(
                request.data,
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
