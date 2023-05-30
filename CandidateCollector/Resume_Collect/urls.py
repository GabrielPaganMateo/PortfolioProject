from django.urls import path
from . import views

urlpatterns = [
    path('', views.LogIn, name="LogIn"),
    path('Collection/', views.Collection, name="Collection"),
    path('Resume/<str:pk>/', views.Resume, name="Resume"),
]