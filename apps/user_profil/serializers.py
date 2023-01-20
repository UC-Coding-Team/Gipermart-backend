from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import (
    User,
    ProfileFeedItem
)

class UserProfileSerializer(serializers.ModelSerializer):
    """A Serializer for our user profile objects."""

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """A serializer for profile feed items."""

    class Meta:
        model = ProfileFeedItem
        fields = ('id', 'user_profile','status_text','created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}