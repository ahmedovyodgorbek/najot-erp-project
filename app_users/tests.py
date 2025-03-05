from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateAPITestCase(APITestCase):

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpass', role='admin'
        )
        self.admin_token = RefreshToken.for_user(self.admin_user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.url = reverse('users:register')  # Make sure this is the correct URL name

    def test_create_user_success(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'phone_number': '+1234567890',
            'role': 'student',
            'gender': 'male',
            'password': 'securepass123',
            'password2': 'securepass123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(username='johndoe').exists())

    def test_create_user_password_mismatch(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe',
            'phone_number': '+1234567890',
            'role': 'teacher',
            'gender': 'female',
            'password': 'securepass123',
            'password2': 'differentpass'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords do not match!', response.data['non_field_errors'])

    def test_create_user_unauthorized(self):
        self.client.credentials()  # Remove authentication
        data = {
            'first_name': 'Mark',
            'last_name': 'Smith',
            'username': 'marksmith',
            'phone_number': '+1234567890',
            'role': 'student',
            'gender': 'male',
            'password': 'securepass123',
            'password2': 'securepass123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # IsAdminUser should block access
