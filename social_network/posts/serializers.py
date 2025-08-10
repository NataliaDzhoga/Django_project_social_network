from rest_framework import serializers
from .models import Post, Like, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user',]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'comment', 'time_comment']
        read_only_fields = ['user',]

    def create(self, validated_data):
        user = self.context.get('request').user
        print("Authenticated user:", user)
        validated_data['user'] = user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', ]
        read_only_fields = ['user', ]

    def create(self, validated_data):
        user = self.context.get('request').user
        print("Authenticated user:", user)
        validated_data['user'] = user
        return super().create(validated_data)


class PostCommSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'post', 'photo', 'add_time', 'comments', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()
