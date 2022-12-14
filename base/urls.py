from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),

    path('show-room/<str:pk>/', views.showRoom, name="show-room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('topics/', views.mobileTopics, name="mobile-topics"),
    path('activity/', views.showActivity, name="activity"),



]
