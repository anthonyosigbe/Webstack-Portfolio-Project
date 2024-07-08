from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserPreference
import os
import json
from django.conf import settings

# This tests.py file includes tests for:
# Viewing the user preferences index page via a GET request.
# Posting a new currency preference when a preference already exists.
# Posting a new currency preference when no preference exists yet.

class UserPreferenceTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.currency_data = {
            "USD": "United States Dollar",
            "EUR": "Euro",
            "NGN": "Nigerian Naira"
        }
        self.file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        with open(self.file_path, 'w') as json_file:
            json.dump(self.currency_data, json_file)
        self.user_preference = UserPreference.objects.create(user=self.user, currency='USD')

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_index_view_get(self):
        response = self.client.get(reverse('preferences'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'preferences/index.html')
        self.assertContains(response, 'United States Dollar')
        self.assertEqual(response.context['user_preferences'].currency, 'USD')

    def test_index_view_post_existing_preference(self):
        response = self.client.post(reverse('preferences'), {
            'currency': 'EUR'
        })
        self.assertEqual(response.status_code, 200)
        self.user_preference.refresh_from_db()
        self.assertEqual(self.user_preference.currency, 'EUR')
        self.assertContains(response, 'Changes saved')

    def test_index_view_post_new_preference(self):
        self.user_preference.delete()
        response = self.client.post(reverse('preferences'), {
            'currency': 'NGN'
        })
        self.assertEqual(response.status_code, 200)
        user_preference = UserPreference.objects.get(user=self.user)
        self.assertEqual(user_preference.currency, 'NGN')
        self.assertContains(response, 'Changes saved')
