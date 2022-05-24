from dataclasses import fields
from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our api view"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password':{
                'write_only': True,    # u can only use it to create new obj, we use extra kwargs to specify more modifications to a certain field
                'style':{'input_type':'password'} # stars when tpying the password
            }
        }
    
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user