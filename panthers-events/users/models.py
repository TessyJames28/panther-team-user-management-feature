from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, id, name, email, access_token, refresh_token, avatar):
        user = self.model(id=id, name=name, email=email, access_token=access_token, refresh_token=refresh_token, avatar=avatar)
        user.save()
        return user

    def create_superuser(self, id, name, email, access_token, refresh_token, avatar):
        user = self.create_user(id=id, name=name, email=email, access_token=access_token, refresh_token=refresh_token, avatar=avatar)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=60, primary_key=True)
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=120)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name', 'email', 'access_token', 'refresh_token', 'avatar']
    
    def __str__(self):
        return self.name