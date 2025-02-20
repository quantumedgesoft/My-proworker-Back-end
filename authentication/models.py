from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Client', 'Client'),
    )
    username = models.CharField(max_length=30, unique=True, validators=[UnicodeUsernameValidator])
    email = models.EmailField(max_length=40, unique=True)
    user_type = models.CharField(max_length=25, choices=USER_TYPE)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    
    def save(self, *args, **kwargs):
        if self.user_type == 'Admin':
            self.is_superuser = True
            self.is_staff = True
        if self.user_type == 'Staff':
            self.is_staff = True
        if self.user_type == 'Client':
            self.is_superuser = False
            self.is_staff = False
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email


class AdminModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_user')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=25)
    profile_picture = models.ImageField(upload_to='client/profile-picture/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.first_name+ ' ' + self.last_name


class ClientModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client_user')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=25)
    profile_picture = models.ImageField(upload_to='client/profile-picture/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.first_name+ ' ' + self.last_name


class FreelancerProfile(models.Model):
    profile = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name='client_freelancer_profile')
    professional_heading = models.CharField(max_length=500, blank=True, null=True)
    top_skills = models.CharField(max_length=500)
    summary = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Freelancer Profile of {self.profile}'


class BuyerProfile(models.Model):
    profile = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name='client_buyer_profile')
    about = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Buyer Profile of {self.profile}'

