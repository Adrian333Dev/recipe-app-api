# Serialzers for user API views

from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # extra_kwargs to make password write only
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        # create_user is a helper function in the User model
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # pop is a helper function to remove password from validated_data
        password = validated_data.pop('password', None)
        # super() calls the ModelSerializer's update function
        user = super().update(instance, validated_data)

        # set_password is a helper function in the User model
        if password:
            user.set_password(password)
            user.save()

        return user
