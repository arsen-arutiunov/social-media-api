from rest_framework import serializers

from social_media.models import Post, Profile, Follow, Hashtag, Like, Comment


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "bio", "profile_picture", "created_at", "updated_at"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        slug_field="name", queryset=Hashtag.objects.all(), many=True
    )

    class Meta:
        model = Post
        fields = [
            "id", "content", "media", "hashtags", "created_at", "updated_at"
        ]

    def create(self, validated_data):
        hashtags = validated_data.pop("hashtags", [])
        post = Post.objects.create(**validated_data)
        post.hashtags.set(hashtags)
        return post


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ["id", "name", "created_at"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "post", "content", "created_at", "updated_at"]
