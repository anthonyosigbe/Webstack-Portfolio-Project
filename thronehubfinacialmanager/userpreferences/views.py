from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages

# View function for handling user preferences index page

def index(request):
    # Initialize an empty list to store currency data
    currency_data = []
    
    # Construct the file path to the currencies.json file
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    # Open and read the currencies.json file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        # Iterate over the items in the JSON data and append them to currency_data list
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    # Check if there exists a UserPreference object for the current user
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        # Retrieve the UserPreference object for the current user
        user_preferences = UserPreference.objects.get(user=request.user)

    # Handle GET request: Render preferences/index.html template with currency data and user preferences
    if request.method == 'GET':
        return render(request, 'preferences/index.html', {'currencies': currency_data,
                                                          'user_preferences': user_preferences})
    else:
        # Handle POST request: Update or create UserPreference object based on form data
        currency = request.POST['currency']
        if exists:
            # Update existing UserPreference with new currency value
            user_preferences.currency = currency
            user_preferences.save()
        else:
            # Create a new UserPreference object with the selected currency
            UserPreference.objects.create(user=request.user, currency=currency)

        # Display success message and render preferences/index.html template with updated data
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})
