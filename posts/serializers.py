from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        source='author.username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ['author']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        source='author.username',
        read_only=True
    )
    post = serializers.PrimaryKeyRelatedField(
        source='post.id',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ['author']
