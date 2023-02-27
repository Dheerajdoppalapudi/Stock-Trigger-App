from django.urls import path

from . import views

urlpatterns = [
    path('users/register/', views.registersUser, name='register'),
    path('users/login/', views.loginUser, name='login'),
    path('users/logout/', views.logoutRequest, name='logout'),
]
