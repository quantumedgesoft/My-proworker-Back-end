from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import AuthenticationFailed


# =====Admin User Creation & Login Token Serializers Start===
class AdminUserCreationSerializers(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'username', 'password', 'user_type']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        user = CustomUser.objects.create(
            username = validated_data['password'],
            email = validated_data['email'],
            password = validated_data['password'],
            user_type = validated_data['user_type']
        )
        return user

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.user_type == 'Client':
            raise AuthenticationFailed("Only Admin, Super Admin or Staff can login!", code='authorization')
        return data
# =====Admin User Creation & Login Token Serializers End===


# =====Client User Creation & Login Token Serializers Start===
class ClientRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        validated_data['user_type'] = "Client"
        user = CustomUser.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            user_type = validated_data['user_type']
        )
        return user

class ClientTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.user_type != 'Client':
            raise AuthenticationFailed("Only Client can login!", code='authorization')
        return data
# =====Client User Creation & Login Token Serializers End===

