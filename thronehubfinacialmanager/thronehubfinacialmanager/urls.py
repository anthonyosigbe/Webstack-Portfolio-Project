"""
URL configuration for thronehubfinacialmanager project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('expenses.urls')),
    path('authentication/', include('authentication.urls')),
    path('preferences/', include('userpreferences.urls')),
    path('income/', include('userincome.urls')),
    path('admin/', admin.site.urls),
]
