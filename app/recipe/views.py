# Views for recipe API

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    # Queryset is used to retrieve objects from the database
    queryset = Recipe.objects.all()
    # Add authentication and permission classes
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Override the get_queryset function to return objects for the
    # authenticated user only
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # Return objects for the current authenticated user only
        return self.queryset.filter(user=self.request.user).order_by('-id')

    # Override the perform_create function to add the user to the recipe
    # object
    def perform_create(self, serializer):
        """Create a new recipe"""
        # Create a new recipe
        serializer.save(user=self.request.user)
