from django.db import models
from django.contrib.auth.models import User

# UserPreference model representing user-specific preferences

class UserPreference(models.Model):
    # One-to-one relationship with the User model, ensuring each user has a single preference set
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    # Field to store the preferred currency, allowing blank values and null values
    currency = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # String representation of the model instance, showing the user's preferences
        return str(self.user) + "'s preferences"
