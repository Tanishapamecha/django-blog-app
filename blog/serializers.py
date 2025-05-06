from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author', 'post', 'updated_at']
        read_only_fields = ['author', 'post']  # Make 'author' and 'post' read-only


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author', 'comments']
        # The 'author' field should not be included in the request since we are handling it in the view
        read_only_fields = ['author']

    def create(self, validated_data):
        # Set the author to the currently logged-in user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
