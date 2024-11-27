from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets


from social_media.models import (
    Post,
    Profile,
    Follow,
    Like,
    Comment, Hashtag,
)
from social_media.serializers import (
    ProfileSerializer,
    FollowSerializer,
    PostSerializer,
    LikeSerializer,
    CommentSerializer, HashtagSerializer,
)



class ProfileViewSet(viewsets.GenericViewSet,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.request.user.profile


class FollowViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    def get_object(self):
        following_id = self.kwargs.get("pk")
        return Follow.objects.get(follower=self.request.user,
                                  following_id=following_id)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LikeViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    retrieve=extend_schema(
        summary="Get a comment by id",
        description="Get a comment by ID."
    ),
    update=extend_schema(
        summary="Update a comment by id",
        description="Update a comment by ID."
    ),
    partial_update=extend_schema(
        summary="Partial update a comment by id",
        description="Partially update comment by ID."
    ),
    destroy=extend_schema(
        summary="Delete a comment by id",
        description="Delete a comment by ID."
    )
)
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Get comments",
        description="Returns the comments of the post",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a comment",
        description="Creates a new comment",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
