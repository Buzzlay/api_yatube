from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnlyPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnlyPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        post = self.get_object()
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
        post = self.get_object()
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnlyPermission]

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
        comment = self.get_object()
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
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
