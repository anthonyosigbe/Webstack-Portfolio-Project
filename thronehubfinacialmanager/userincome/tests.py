from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserIncome, Source
from userpreferences.models import UserPreference
from datetime import date
import json

# This tests.py file includes tests for:
# Searching income records.
# Viewing the income index page.
# Adding an income record via GET and POST requests.
# Editing an income record via GET and POST requests.
# Deleting an income record.

class UserIncomeTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.source = Source.objects.create(name='Salary')
        self.user_preference = UserPreference.objects.create(user=self.user, currency='USD')
        self.income = UserIncome.objects.create(
            amount=5000,
            date=date.today(),
            description='Monthly salary',
            owner=self.user,
            source=self.source.name
        )

    def test_search_income(self):
        response = self.client.post(
            reverse('search_income'), 
            data=json.dumps({'searchText': 'salary'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Monthly salary', str(response.content))

    def test_index_view(self):
        response = self.client.get(reverse('income'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income/index.html')
        self.assertContains(response, 'Monthly salary')

    def test_add_income_get(self):
        response = self.client.get(reverse('add-income'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income/add_income.html')

    def test_add_income_post(self):
        response = self.client.post(reverse('add-income'), {
            'amount': 3000,
            'description': 'Freelance work',
            'income_date': date.today(),
            'source': self.source.name
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful addition
        self.assertTrue(UserIncome.objects.filter(description='Freelance work').exists())

    def test_income_edit_get(self):
        response = self.client.get(reverse('income-edit', args=[self.income.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income/edit_income.html')

    def test_income_edit_post(self):
        response = self.client.post(reverse('income-edit', args=[self.income.id]), {
            'amount': 6000,
            'description': 'Updated salary',
            'income_date': date.today(),
            'source': self.source.name
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.income.refresh_from_db()
        self.assertEqual(self.income.amount, 6000)
        self.assertEqual(self.income.description, 'Updated salary')

    def test_delete_income(self):
        response = self.client.post(reverse('income-delete', args=[self.income.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(UserIncome.objects.filter(id=self.income.id).exists())
