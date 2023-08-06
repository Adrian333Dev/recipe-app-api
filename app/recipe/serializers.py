# Serializers for recipe API

from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    # Meta class is a configuration for the serializer
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'price', 'link')
        # Make sure that the id is read only
        read_only_fields = ('id',)
