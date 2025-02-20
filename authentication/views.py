from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import AdminTokenObtainPairSerializer, ClientTokenObtainPairSerializer, AdminUserCreationSerializers, ClientRegistrationSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .models import ClientModel, AdminModel


# =====Admin User Creation & Login Token views Start===
class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

class AdminCreationViews(CreateAPIView):
    serializer_class = AdminUserCreationSerializers
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        AdminModel.objects.create(
            user=user,
            first_name = request.data['name']
        ).save()
        return Response(
            {
                'message': 'User Creation Successfully!'
            }, status=status.HTTP_201_CREATED
        )

# =====Admin User Creation & Login Token views End===


# =====Client User Creation & Login Token Views Start===
class ClientTokenObtainPairView(TokenObtainPairView):
    serializer_class = ClientTokenObtainPairSerializer

class ClientRegistrationViews(CreateAPIView):
    serializer_class = ClientRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        ClientModel.objects.create(
            user = user,
            first_name = request.data['first_name'],
            last_name = request.data['last_name']
        ).save()
        return Response(
            {
                'message': 'Registration Successfully!'
            }, status=status.HTTP_201_CREATED
        )
# =====Client User Creation & Login Token Views End===



