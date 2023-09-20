from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class User(models.Model):
    id = models.CharField(max_length=60, primary_key=True)
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=120)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name', 'email', 'access_token', 'refresh_token', 'avatar']
    
    def __str__(self):
        return self.name
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True