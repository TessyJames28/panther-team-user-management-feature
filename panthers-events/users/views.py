from django.shortcuts import render,redirect
from rest_framework import generics
from rest_framework.response import Response
from django.views import View
from .serializers import UserSerializer
from .models import User
from authlib.integrations.django_client import OAuth
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from rest_framework.views import APIView
import uuid
from django.conf import settings
from itsdangerous import URLSafeTimedSerializer
from django.http import HttpResponseForbidden


CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile',
    },
    authorize_params={'access_type': 'offline'},
)

class AuthenticationMiddleware(APIView):
    serializer_class = UserSerializer  # Assuming the UserSerializer is already defined
    secret_key = settings.SECRET_KEY  # Replace with your actual secret key

    def check_authentication(self, request):
        # token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1] # this code will retreive from the header though I am not sure of the key it will bear
        token = request.GET.get('session_token') # currently, the token appears as a query parameter. This code gets it from there

        if not token:
            return None

        serializer = URLSafeTimedSerializer(self.secret_key)
        user_id = serializer.loads(token, max_age=3600)  # Adjust expiration time if needed

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                return user
            except User.DoesNotExist:
                pass

        return None

    def dispatch(self, request, *args, **kwargs):
        user = self.check_authentication(request)

        if not user:
            return HttpResponseForbidden()

        request.user = user
        return super().dispatch(request, *args, **kwargs)
    
    
# Create your views here.
class UserView(AuthenticationMiddleware, generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class SingleUserView(AuthenticationMiddleware, generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    lookup_field = 'id'  # Set the lookup field to 'id'
    
    
class LoginView(View):
    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse('auth'))
        return oauth.google.authorize_redirect(request, redirect_uri)

class AuthView(View):
    def get(self, request):
        token = oauth.google.authorize_access_token(request)

        User = get_user_model()
        email = token.get('userinfo', {}).get('email')
        name = token.get('userinfo', {}).get('name')
        picture = token.get('userinfo', {}).get('picture')
        access_token = token.get('access_token', {})
        
        user, created = User.objects.get_or_create(email=email)
        user.access_token = access_token
        user.is_active = True
        user.save()
        
        if created:
            user.name = name
            user.avatar = picture
            user.save()

        # Generate a session token
        serializer = URLSafeTimedSerializer(AuthenticationMiddleware.secret_key)
        session_token = serializer.dumps(str(user.id))

        redirect_uri = request.build_absolute_uri(reverse('user_detail', kwargs={"id": user.id}))
        
        # Redirect with the session token as a query parameter
        redirect_uri += '?session_token=' + session_token
        return redirect(redirect_uri)
    
