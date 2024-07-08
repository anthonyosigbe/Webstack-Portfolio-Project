from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Expense, Category
import json
import datetime
from django.utils.timezone import now

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.expense = Expense.objects.create(
            amount=100.0,
            date=now(),
            description='Test description',
            owner=self.user,
            category=self.category.name
        )
        self.client.login(username='testuser', password='12345')

    def test_index_GET(self):
        response = self.client.get(reverse('expenses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/index.html')

    def test_add_expense_GET(self):
        response = self.client.get(reverse('add-expenses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/add_expense.html')

    def test_add_expense_POST(self):
        response = self.client.post(reverse('add-expenses'), {
            'amount': 200.0,
            'description': 'Another test description',
            'expense_date': '2024-01-01',
            'category': self.category.name
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.last().amount, 200.0)

    def test_edit_expense_GET(self):
        response = self.client.get(reverse('expense-edit', args=[self.expense.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/edit-expense.html')

    def test_edit_expense_POST(self):
        response = self.client.post(reverse('expense-edit', args=[self.expense.id]), {
            'amount': 300.0,
            'description': 'Updated description',
            'expense_date': '2024-01-02',
            'category': self.category.name
        })
        self.assertEqual(response.status_code, 302)
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.amount, 300.0)

    def test_delete_expense(self):
        response = self.client.get(reverse('expense-delete', args=[self.expense.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Expense.objects.filter(id=self.expense.id).exists())

    def test_search_expenses(self):
        response = self.client.post(reverse('search_expenses'), {
            'searchText': 'Test'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test description', str(response.content))

    def test_expense_category_summary(self):
        response = self.client.get(reverse('expense_category_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Category', str(response.content))

    def test_stats_view(self):
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/stats.html')

    def test_export_csv(self):
        response = self.client.get(reverse('export-csv'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response['Content-Type'])

    def test_export_excel(self):
        response = self.client.get(reverse('export-excel'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/ms-excel', response['Content-Type'])

class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.expense = Expense.objects.create(
            amount=100.0,
            date=now(),
            description='Test description',
            owner=self.user,
            category=self.category.name
        )

    def test_expense_str(self):
        self.assertEqual(str(self.expense), self.category.name)

    def test_category_str(self):
        self.assertEqual(str(self.category), self.category.name)
