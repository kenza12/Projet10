from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User

class UserTests(APITestCase):
    def setUp(self):
        """
        Set up function to initialize test environment.
        This function is executed before each test.
        """

        # Initialize APIClient for making API requests
        self.client = APIClient()

        # User data for creating test users
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
            "age": 20,
            "can_be_contacted": True,
            "can_data_be_shared": False
        }

        # Create a superuser for admin-related tests
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'adminpassword', age=30)
    
    def test_create_user(self):
        """
        Test to ensure that a new user can be successfully created.
        """

        # Make a POST request to the signup endpoint
        response = self.client.post(reverse('signup'), self.user_data, format='json')

        # Check that the response status is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if a new user is added to the database
        self.assertEqual(User.objects.count(), 2)

        # Ensure the user with the provided username exists
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_access_own_profile(self):
        """
        Test to ensure that a user can access their own profile.
        """
        # Create a user before testing access
        self.client.post(reverse('signup'), self.user_data, format='json')
        user = User.objects.get(username='testuser')

        # Authenticate as the user
        self.client.force_authenticate(user=user)

        # Make a GET request to the user's profile
        response = self.client.get(reverse('user-detail', kwargs={'pk': user.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_own_profile(self):
        """
        Test to ensure that a user can update their own profile.
        """
        # Create a user first
        self.client.post(reverse('signup'), self.user_data, format='json')
        user = User.objects.get(username='testuser')

        # Authenticate as the user
        self.client.force_authenticate(user=user)

        # Update user profile
        updated_data = {'age': 25, 'can_be_contacted': False}
        response = self.client.patch(reverse('user-detail', kwargs={'pk': user.id}), updated_data)

        # Check that the response status is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh user data from the database and validate the changes
        user.refresh_from_db()
        self.assertEqual(user.age, 25)
        self.assertEqual(user.can_be_contacted, False)

    def test_admin_access_user_profile(self):
        """
        Test to ensure that an admin user can access any user's profile.
        """
        # Create a regular user first
        self.client.post(reverse('signup'), self.user_data, format='json')
        user = User.objects.get(username='testuser')

        # Authenticate as the admin user
        self.client.force_authenticate(user=self.admin_user)

        # Admin user accesses the regular user's profile
        response = self.client.get(reverse('user-detail', kwargs={'pk': user.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        """
        Test to ensure that a user can delete their own profile.
        """
        # Create a user first
        self.client.post(reverse('signup'), self.user_data, format='json')
        user = User.objects.get(username='testuser')
        
        # Authenticate as the user
        self.client.force_authenticate(user=user)

        # Make a DELETE request to remove the user
        response = self.client.delete(reverse('user-detail', kwargs={'pk': user.id}))

        # Check that the response status is 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the user no longer exists in the database
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_user_age_validation(self):
        """
        Ensure a user must be at least 15 years old to register.
        """
        young_user_data = {
            "username": "younguser",
            "password": "password123",
            "password_confirm": "password123",
            "age": 14,  # Age less than 15
            "can_be_contacted": True,
            "can_data_be_shared": False
        }
        response = self.client.post(reverse('signup'), young_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Users must be at least 15 years old.', str(response.content))
    
    def test_non_admin_access_denied(self):
        """
        Ensure non-admin users cannot access other users' profiles.
        """
        # Create user1
        self.client.post(reverse('signup'), self.user_data, format='json')
        user1 = User.objects.get(username='testuser')

        # Create user2 with different username
        user2_data = self.user_data.copy()
        user2_data['username'] = 'user2'
        self.client.post(reverse('signup'), user2_data, format='json')
        user2 = User.objects.get(username='user2')

        # User1 tries to access User2's profile
        self.client.force_authenticate(user=user1)
        response = self.client.get(reverse('user-detail', kwargs={'pk': user2.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)