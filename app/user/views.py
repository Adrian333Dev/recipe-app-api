# Views for the User API.

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    # renderer_classes is a tuple of all the renderers that are enabled
    # for this view
    serializer_class = AuthTokenSerializer
    # renderer_classes is a tuple of all the renderers that are enabled
    # for this view
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
