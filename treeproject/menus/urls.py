from django.shortcuts import render
from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='home'),
]