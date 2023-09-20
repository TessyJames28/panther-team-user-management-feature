from django.urls import path
from . import views
from .views import LoginView, AuthView

urlpatterns = [
    path('api/user', views.UserView.as_view()),
    path('api/user/<str:id>', views.SingleUserView.as_view(),name="user_detail"),
    path('login/', LoginView.as_view(), name='login'),
    path('auth/', AuthView.as_view(), name='auth'),
]