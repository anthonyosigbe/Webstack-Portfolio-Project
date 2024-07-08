"""
URL configuration for thronehubfinacialmanager project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Include URLs from 'expenses' app
    path('', include('expenses.urls')),
    
    # Include URLs from 'authentication' app
    path('authentication/', include('authentication.urls')),
    
    # Include URLs from 'userpreferences' app
    path('preferences/', include('userpreferences.urls')),
    
    # Include URLs from 'userincome' app
    path('income/', include('userincome.urls')),
    
    # Admin site URL
    path('admin/', admin.site.urls),
]
