from django.urls import path, include
from rest_framework import routers

from social_media.views import (
    ProfileViewSet,
    PostViewSet,
    HashtagViewSet,
    LikeViewSet,
    CommentViewSet,
    FollowViewSet,
)

router = routers.DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"follow", FollowViewSet, basename="follow")
router.register(r"posts", PostViewSet, basename="post")
router.register(r"hashtags", HashtagViewSet, basename="hashtag")
router.register(r"likes", LikeViewSet, basename="like")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [path("", include(router.urls))]

app_name = "social_media"
