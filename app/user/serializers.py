# Serialzers for user API views

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

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


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    # email and password are required fields
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        # attrs is a dictionary of all the fields that make up the serializer
        email = attrs.get('email')
        password = attrs.get('password')
        # authenticate() is a Django helper function
        user = authenticate(
            # context is a dictionary of the request object
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            # if authentication fails, raise an error
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        # set the user in the attrs dictionary
        attrs['user'] = user
        return attrs
