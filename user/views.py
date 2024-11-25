from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Create a new user",
        description=(
            "Allows a new user to register by providing "
            "their details such as username, email, and password. "
            "Returns the newly created user's data."
        ),
        responses={201: UserSerializer},
    )
)
class CreateUserView(generics.CreateAPIView):
    """Endpoint to register a new user"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Endpoint to log in and retrieve an auth token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve current user's profile",
        description="Fetches the authenticated user's profile data.",
        responses={200: UserSerializer},
    ),
    put=extend_schema(
        summary="Update current user's profile",
        description="Allows the authenticated user to "
                    "update their profile information.",
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
    patch=extend_schema(
        summary="Partially update current user's profile",
        description="Allows the authenticated user to partially "
                    "update their profile information.",
        request=UserSerializer,
        responses={200: UserSerializer},
    )
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Endpoint to manage the authenticated user's profile"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
