from django.contrib import admin
from .models import UserIncome, Source

# Registering models for administration

admin.site.register(UserIncome)
admin.site.register(Source)