from django.urls import path
from . import views

urlpatterns = [
    path('api/user', views.UserView.as_view()),
    path('api/user/<str:id>', views.SingleUserView.as_view()),
    
]