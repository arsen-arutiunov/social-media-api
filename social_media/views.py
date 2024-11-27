from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter
)
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from social_media.models import (
    Post,
    Profile,
    Follow,
    Like,
    Comment,
    Hashtag,
)
from social_media.serializers import (
    ProfileSerializer,
    FollowSerializer,
    PostSerializer,
    LikeSerializer,
    CommentSerializer,
    HashtagSerializer,
    ProfileListSerializer,
)
from user.models import User


@extend_schema_view(
    list=extend_schema(
        summary="Get list of profiles",
        description="Return list of profiles.",
        parameters=[
            OpenApiParameter(
                name="username",
                type={"type": "string"},
                description="Full or part of username of the profile",
            )
        ],
    ),
    create=extend_schema(
        summary="Create a new profile",
        description="Create a new profile.",
    ),
    retrieve=extend_schema(
        summary="Get a profile by id",
        description="Return a profile by id.",
    ),
    update=extend_schema(
        summary="Update a profile by id",
        description="Update a profile by id.",
    ),
    partial_update=extend_schema(
        summary="Partial update a profile by id",
        description="Partially update a profile by id.",
    ),
    destroy=extend_schema(
        summary="Delete a profile by id",
        description="Delete a profile by id.",
    )
)
class ProfileViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        username = self.request.query_params.get("username")
        queryset = self.queryset

        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        return ProfileSerializer

    def get_object(self):
        profile = super().get_object()
        if (
            self.action in ["update", "partial_update", "destroy"]
            and profile.user != self.request.user
        ):
            raise PermissionDenied("You can only edit your profile.")
        return profile


@extend_schema_view(
    destroy=extend_schema(
        summary="Delete a follow",
        description="This endpoint deletes a follow.",
    ),
    list=extend_schema(
        summary="Get follows",
        description="Returns the follows",
    ),
    create=extend_schema(
        summary="Create a follow",
        description="Creates a new follow",
    ),
)
class FollowViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        following = serializer.validated_data.get("following")
        if Follow.objects.filter(
            follower=self.request.user, following=following
        ).exists():
            raise ValidationError("You are already subscribed to this user.")
        serializer.save(follower=self.request.user)

    def destroy(self, request, *args, **kwargs):

        instance = get_object_or_404(
            Follow,
            follower=self.request.user,
            following_id=kwargs.get("pk"),
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def _get_follow_queryset(user, related_name):
        return User.objects.filter(**{f"{related_name}__follower": user}).distinct()

    def following_list(self, request, *args, **kwargs):
        queryset = self._get_follow_queryset(request.user, "following")
        return Response({"following": [user.email for user in queryset]})

    def followers_list(self, request, *args, **kwargs):
        queryset = self._get_follow_queryset(request.user, "followers")
        return Response({"followers": [user.email for user in queryset]})


@extend_schema_view(
    retrieve=extend_schema(
        summary="Get a post by id",
        description="Return a post by id.",
    ),
    update=extend_schema(
        summary="Update a post by id",
        description="Update a post by id.",
    ),
    partial_update=extend_schema(
        summary="Partial update a post by id",
        description="Partially update a post by id.",
    ),
    destroy=extend_schema(
        summary="Delete a post by id",
        description="This endpoint deletes a post by id.",
    ),
    create=extend_schema(
        summary="Create a post",
        description="Creates a new post.",
    ),
    list=extend_schema(
        summary="Get list of posts",
        description="Returns the list of posts.",
    ),
)
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.values_list("following", flat=True)
        return Post.objects.filter(
            user__id__in=following_users
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Get my posts",
        description="Returns my posts.",
    )
    @action(detail=False, methods=["get"], url_path="my-posts")
    def my_posts(self, request):
        posts = Post.objects.filter(user=request.user).order_by("-created_at")
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get posts by hashtag",
        description="Returns the posts by hashtag.",
        parameters=[
            OpenApiParameter(
                name="hashtag",
                type={"type": "string"},
                required=True,
                description="The hashtag of the post.",
            )
        ]
    )
    @action(detail=False, methods=["get"], url_path="hashtag-posts")
    def hashtag_posts(self, request):
        hashtag = request.query_params.get("hashtag")
        if hashtag:
            posts = Post.objects.filter(
                hashtags__name=hashtag
            ).order_by("-created_at")
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        return Response({"detail": "Hashtag not provided"}, status=400)


@extend_schema_view(
    retrieve=extend_schema(
        summary="Get a hashtag by id", description="Return a hashtag by ID."
    ),
    update=extend_schema(
        summary="Update a hashtag by id", description="Update a hashtag by ID."
    ),
    partial_update=extend_schema(
        summary="Partial update a hashtag by id",
        description="Partially update hashtag by ID.",
    ),
    destroy=extend_schema(
        summary="Delete a hashtag by id", description="Delete a hashtag by ID."
    ),
    create=extend_schema(summary="Create a hashtag", description="Create new hashtag."),
    list=extend_schema(summary="List all hashtags", description="Return all hashtags."),
)
class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@extend_schema_view(
    destroy=extend_schema(
        summary="Delete a like",
        description="This endpoint deletes a like.",
    ),
    list=extend_schema(
        summary="Get likes",
        description="Returns the likes of the post",
    ),
    create=extend_schema(
        summary="Create a like",
        description="Creates a new like",
    ),
)
class LikeViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        post = serializer.validated_data["post"]
        user = self.request.user

        if Like.objects.filter(user=user, post=post).exists():
            raise ValidationError("You have already liked this post.")
        serializer.save(user=user)


@extend_schema_view(
    retrieve=extend_schema(
        summary="Get a comment by id", description="Get a comment by ID."
    ),
    update=extend_schema(
        summary="Update a comment by id", description="Update a comment by ID."
    ),
    partial_update=extend_schema(
        summary="Partial update a comment by id",
        description="Partially update comment by ID.",
    ),
    destroy=extend_schema(
        summary="Delete a comment by id", description="Delete a comment by ID."
    ),
    list=extend_schema(
        summary="Get comments",
        description="Returns the comments of the post",
    ),
    create=extend_schema(
        summary="Create a comment",
        description="Creates a new comment",
    ),
)
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
