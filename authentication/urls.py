from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import AdminCreationViews, AdminTokenObtainPairView, ClientRegistrationViews, ClientTokenObtainPairView

urlpatterns = [
    path('auth/login/', ClientTokenObtainPairView.as_view(), name='auth-token'),
    path('auth/registration/', ClientRegistrationViews.as_view(), name='client-registration'),
    path('auth/admin-login/', AdminTokenObtainPairView.as_view(), name='admin-auth-token'),
    path('auth/user-create/', AdminCreationViews.as_view(), name='admin-user-create'),
]
