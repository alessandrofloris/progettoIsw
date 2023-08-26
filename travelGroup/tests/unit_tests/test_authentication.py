import unittest

from django.test import TestCase, Client
from travelGroup.models import CustomUser
from django.urls import reverse
from travelGroup.forms import RegistrationUserForm, AuthenticationForm


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('travelGroup:login')
        self.logout_url = reverse('travelGroup:logout')
        self.registration_url = reverse('travelGroup:signup')
        self.mytrips_url = reverse('travelGroup:mytrips')
        self.user_data_test = {
            'username': 'newuser',
            'password1': 'Password#1',
            'password2': 'Password#1',
            'email': 'testuser@gmail.com',
            'first_name': 'new',
            'last_name': 'user',
        }

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'travelGroup/login.html')
        self.assertIsInstance(response.context['authenticationForm'], AuthenticationForm)

    def test_login_view_post_success(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, self.mytrips_url)
        self.assertEqual(response.status_code, 302)

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'travelGroup/login.html')
        self.assertIsInstance(response.context['authenticationForm'], AuthenticationForm)
        # self.assertEqual(response.context['login_error'], 'Login fallito')

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertEqual(response.status_code, 302)

    def test_signup_view_get(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'travelGroup/registration.html')
        self.assertIsInstance(response.context['registrationUserForm'], RegistrationUserForm)

    def test_signup_view_post_valid_form(self):
        response = self.client.post(self.registration_url, self.user_data_test)
        self.assertRedirects(response, self.login_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username=self.user_data_test['username']).exists())

    def test_signup_view_post_invalid_form(self):
        new_user_not_valid = {
            'username': 'invaliduser',
            'password1': 'Testpassword#1',
            'password2': 'DifferentPassword#1',  # Password diversa da quella sopra
            'email': 'testuser@example.com',
            'first_name': 'invalid',
            'last_name': 'user',
        }
        response = self.client.post(self.registration_url, new_user_not_valid)

        # Verifica che la risposta non sia un reindirizzamento, ma un render della stessa pagina di registrazione
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'travelGroup/registration.html')
        self.assertFalse(response.context['registrationUserForm'].is_valid())
        self.assertFalse(CustomUser.objects.filter(username=new_user_not_valid['username']).exists())


if __name__ == '__main__':
    unittest.main()
