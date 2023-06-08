from django.urls import path
from . import views

urlpatterns = [
    path('Register/', views.Register, name="Register"),
    path('Access/', views.Access, name="Access"),
    path('Collection/', views.Collection, name="Collection"),
    path('Resume/<str:pk>/', views.Resume, name="Resume"),
    path('Exit', views.Exit, name="Exit")
]