from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .utils import account_activation_token

class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.validate_username_url = reverse('validate-username')
        self.validate_email_url = reverse('validate_email')
        self.activate_url = lambda uidb64, token: reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
        self.request_reset_password_url = reverse('request-password')
        self.reset_password_url = lambda uidb64, token: reverse('reset-user-password', kwargs={'uidb64': uidb64, 'token': token})
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')

    def test_email_validation(self):
        response = self.client.post(self.validate_email_url, {'email': 'invalidemail'}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response = self.client.post(self.validate_email_url, {'email': 'testuser@example.com'}, content_type="application/json")
        self.assertEqual(response.status_code, 409)

        response = self.client.post(self.validate_email_url, {'email': 'newuser@example.com'}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'email_valid': True})

    def test_username_validation(self):
        response = self.client.post(self.validate_username_url, {'username': 'invalid username'}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response = self.client.post(self.validate_username_url, {'username': 'testuser'}, content_type="application/json")
        self.assertEqual(response.status_code, 409)

        response = self.client.post(self.validate_username_url, {'username': 'newuser'}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'username_valid': True})

    def test_registration(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')

        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'short'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Password too short')

    def test_verification(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        response = self.client.get(self.activate_url(uidb64, token))
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_request_password_reset(self):
        response = self.client.post(self.request_reset_password_url, {'email': 'invalidemail'})
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Please supply a valid email')

        response = self.client.post(self.request_reset_password_url, {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'We have sent you an email to reset your password')

    def test_complete_password_reset(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        response = self.client.get(self.reset_password_url(uidb64, token))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/set-newpassword.html')

        response = self.client.post(self.reset_password_url(uidb64, token), {
            'password': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Password reset successful, login with your new password')
