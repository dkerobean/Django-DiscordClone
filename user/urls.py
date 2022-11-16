from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginUser, name='login-user'),
    path('logout/', views.logoutUser, name='logout-user'),
    path('register/', views.registerUser, name='register-user'),

    path('profile/<str:pk>/', views.userProfile, name='profile'),
    path('update-user/', views.updateUser, name='update-user'),






]
