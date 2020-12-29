from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Post
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnlyPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnlyPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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

