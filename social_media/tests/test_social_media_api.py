from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from social_media.models import (
    Profile,
    Follow,
    Post,
    Hashtag,
    Like,
    Comment,
)
from social_media.serializers import (
    ProfileListSerializer,
    ProfileSerializer
)


USER = get_user_model()
PROFILE_URL = reverse("social_media:profile-list")
POST_URL = reverse("social_media:post-list")


def sample_profile(**params):
    defaults = {
        "username": "test",
        "first_name": "test",
        "last_name": "test",
        "bio": "test"
    }
    defaults.update(params)
    return Profile.objects.create(**defaults)


def sample_follow(**params):
    defaults = {}
    defaults.update(params)
    return Follow.objects.create(**defaults)


def sample_post(**params):
    defaults = {
        "content": "test",
    }
    defaults.update(params)
    return Post.objects.create(**defaults)


def sample_hashtag(**params):
    defaults = {
        "name": "test",
    }
    defaults.update(params)
    return Hashtag.objects.create(**defaults)


def sample_like(**params):
    defaults = {}
    defaults.update(params)
    return Like.objects.create(**defaults)


def sample_comment(**params):
    defaults = {
        "content": "test",
    }
    defaults.update(params)
    return Comment.objects.create(**defaults)


def profile_detail_url(profile_id):
    return reverse("social_media:profile-detail", args=[profile_id])


def post_detail_url(post_id):
    return reverse("social_media:post-detail", args=[post_id])


class UnauthenticatedSocialMediaAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedSocialMediaAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = USER.objects.create_user(
            email="test@test.test",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_profile_list(self):
        sample_profile(user=self.user)

        res = self.client.get(PROFILE_URL)
        profiles = Profile.objects.all()
        serializer = ProfileListSerializer(profiles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_profile_by_username(self):
        profile_1 = sample_profile(user=self.user)
        profile_2 = sample_profile(
            user=USER.objects.create_user(
                email="test2@test.test",
                password="testpassword",
            ),
            username="kevin22"
        )

        res = self.client.get(
            PROFILE_URL,
            {"username": "tes"},
        )
        serializer_1 = ProfileListSerializer(profile_1)
        serializer_2 = ProfileListSerializer(profile_2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_1.data, res.data)
        self.assertNotIn(serializer_2.data, res.data)

    def test_retrieve_profile_detail(self):
        profile = sample_profile(user=self.user)

        url = profile_detail_url(profile.pk)

        res = self.client.get(url)

        serializer = ProfileSerializer(profile)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_profile(self):
        payload = {
            "user": self.user.id,
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "bio": "test"
        }

        res = self.client.post(PROFILE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_full_name_property(self):
        profile = sample_profile(user=self.user)
        self.assertEqual(profile.full_name, "test test")

    def test_username_unique(self):
        sample_profile(user=self.user)
        with self.assertRaises(Exception):
            Profile.objects.create(
                user=USER.objects.create_superuser(
                    email="tesss@test.test",
                    password="<PASSWORD>",
                ),
                username="test",  # Duplicate username
                first_name="Another",
                last_name="User",
            )

    def test_bio_blank_null(self):
        profile = Profile.objects.create(
            user=self.user,
            username="anotherprofile",
            first_name="Another",
            last_name="User",
        )
        self.assertEqual(profile.bio, None)

    def test_profile_picture_upload(self):
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"file_content",
            content_type="image/jpeg"
        )
        profile = sample_profile(user=self.user,
                                 profile_picture=image)
        self.assertEqual(profile.profile_picture.name,
                         "profile_pics/test_image.jpg")

