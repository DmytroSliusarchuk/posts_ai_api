from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    """

    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
            "status",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at", "status"]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    """

    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "content",
            "created_at",
            "updated_at",
            "status",
        ]
        read_only_fields = [
            "id",
            "post",
            "author",
            "created_at",
            "updated_at",
            "status",
        ]
