"""
Views for the recipe APIs
"""
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

from core.models import Recipe, Tag
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer, TagSerializer


class RecipeViewSet(ModelViewSet):
    """Viewset for the Recipe model."""

    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == "list":
            return RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)


class TagViewSet(DestroyModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """Viewset for the Tag model."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by("-name")
