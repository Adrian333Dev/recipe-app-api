# Views for the User API.

from rest_framework import generics, authentication, permissions
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


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    # authentication_classes is a tuple of all the authentication classes
    # that are enabled for this view
    authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes is a tuple of all the permission classes that
    # are enabled for this view
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user."""
        # self.request.user is the user that is authenticated for the request
        return self.request.user
