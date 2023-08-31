"""
Serializers for recipe APIs
"""
from rest_framework.serializers import ModelSerializer

from core.models import Recipe


class RecipeSerializer(ModelSerializer):
    """Serializer for the recipe object."""

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link"]
        read_only_fields = ["id"]


class RecipeDetailSerializer(ModelSerializer):
    """Serializer for the recipe detail object."""

    class Meta(RecipeSerializer.Meta):
        model = Recipe
        fields = RecipeSerializer.Meta.fields + ["description"]
        read_only_fields = RecipeSerializer.Meta.read_only_fields
