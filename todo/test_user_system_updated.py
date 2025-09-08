"""
Unit tests for User management system including models, services, and API endpoints.

This test module provides comprehensive test coverage for:
- CustomUser model functionality
- UserService business logic
- UserController API endpoints
- Error handling and edge cases
"""

from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
import json

from .models import CustomUser
from .services import UserService
from .serializers import UserSerializer, UserListSerializer


class UserModelTestCase(TestCase):
    """Test cases for the CustomUser model."""

    def setUp(self):
        """Set up test data for CustomUser model tests."""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'Test user biography'
        }

    def test_user_creation(self):
        """Test creating a user with valid data."""
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.is_active)
        self.assertIsNotNone(user.date_joined)

    def test_user_str_method(self):
        """Test the string representation of CustomUser model."""
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(str(user), 'testuser')

    def test_get_full_name(self):
        """Test the get_full_name method."""
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.get_full_name(), 'Test User')

    def test_get_short_name(self):
        """Test the get_short_name method."""
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.get_short_name(), 'Test')

    def test_username_uniqueness(self):
        """Test that username must be unique."""
        CustomUser.objects.create(**self.user_data)
        
        # Try to create another user with the same username
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'different@example.com'
        
        with self.assertRaises(Exception):  # Database integrity error
            CustomUser.objects.create(**duplicate_data)

    def test_email_uniqueness(self):
        """Test that email must be unique."""
        CustomUser.objects.create(**self.user_data)
        
        # Try to create another user with the same email
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'differentuser'
        
        with self.assertRaises(Exception):  # Database integrity error
            CustomUser.objects.create(**duplicate_data)

    def test_user_ordering(self):
        """Test that users are ordered by date_joined descending."""
        import time
        
        user1 = CustomUser.objects.create(
            username='user1',
            email='user1@example.com',
            first_name='User',
            last_name='One'
        )
        
        # Add a small delay to ensure different timestamps
        time.sleep(0.01)
        
        user2 = CustomUser.objects.create(
            username='user2',
            email='user2@example.com',
            first_name='User',
            last_name='Two'
        )
        
        users = list(CustomUser.objects.all())
        self.assertEqual(users[0], user2)  # Most recent first
        self.assertEqual(users[1], user1)


class UserServiceTestCase(TestCase):
    """Test cases for the UserService class."""

    def setUp(self):
        """Set up test data for UserService tests."""
        self.user_data = {
            'username': 'serviceuser',
            'email': 'service@example.com',
            'first_name': 'Service',
            'last_name': 'User',
            'bio': 'Service test user'
        }

    def test_get_all_users_active_only(self):
        """Test getting all active users."""
        # Create active user
        active_user = CustomUser.objects.create(**self.user_data)
        
        # Create inactive user
        inactive_data = self.user_data.copy()
        inactive_data.update({
            'username': 'inactive',
            'email': 'inactive@example.com',
            'is_active': False
        })
        CustomUser.objects.create(**inactive_data)

        active_users = UserService.get_all_users(active_only=True)
        self.assertEqual(len(active_users), 1)
        self.assertEqual(active_users[0], active_user)

    def test_get_all_users_include_inactive(self):
        """Test getting all users including inactive ones."""
        CustomUser.objects.create(**self.user_data)
        
        inactive_data = self.user_data.copy()
        inactive_data.update({
            'username': 'inactive',
            'email': 'inactive@example.com',
            'is_active': False
        })
        CustomUser.objects.create(**inactive_data)

        all_users = UserService.get_all_users(active_only=False)
        self.assertEqual(len(all_users), 2)

    def test_get_user_by_id_existing(self):
        """Test getting a user by existing ID."""
        user = CustomUser.objects.create(**self.user_data)
        found_user = UserService.get_user_by_id(user.id)
        self.assertEqual(found_user, user)

    def test_get_user_by_id_nonexistent(self):
        """Test getting a user by non-existent ID."""
        found_user = UserService.get_user_by_id(999)
        self.assertIsNone(found_user)

    def test_get_user_by_username_existing(self):
        """Test getting a user by existing username."""
        user = CustomUser.objects.create(**self.user_data)
        found_user = UserService.get_user_by_username('serviceuser')
        self.assertEqual(found_user, user)

    def test_get_user_by_username_nonexistent(self):
        """Test getting a user by non-existent username."""
        found_user = UserService.get_user_by_username('nonexistent')
        self.assertIsNone(found_user)

    def test_get_user_by_email_existing(self):
        """Test getting a user by existing email."""
        user = CustomUser.objects.create(**self.user_data)
        found_user = UserService.get_user_by_email('service@example.com')
        self.assertEqual(found_user, user)

    def test_get_user_by_email_nonexistent(self):
        """Test getting a user by non-existent email."""
        found_user = UserService.get_user_by_email('nonexistent@example.com')
        self.assertIsNone(found_user)

    def test_create_user_valid_data(self):
        """Test creating a user with valid data."""
        user = UserService.create_user(self.user_data)
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.username, 'serviceuser')
        self.assertEqual(user.email, 'service@example.com')

    def test_create_user_missing_required_field(self):
        """Test creating a user with missing required fields."""
        incomplete_data = self.user_data.copy()
        del incomplete_data['username']
        
        with self.assertRaises(ValidationError):
            UserService.create_user(incomplete_data)

    def test_create_user_duplicate_username(self):
        """Test creating a user with duplicate username."""
        UserService.create_user(self.user_data)
        
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'different@example.com'
        
        with self.assertRaises(ValidationError):
            UserService.create_user(duplicate_data)

    def test_create_user_duplicate_email(self):
        """Test creating a user with duplicate email."""
        UserService.create_user(self.user_data)
        
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'differentuser'
        
        with self.assertRaises(ValidationError):
            UserService.create_user(duplicate_data)

    def test_update_user_valid_data(self):
        """Test updating a user with valid data."""
        user = UserService.create_user(self.user_data)
        
        update_data = {'first_name': 'Updated', 'bio': 'Updated bio'}
        updated_user = UserService.update_user(user.id, update_data)
        
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.bio, 'Updated bio')

    def test_update_user_nonexistent(self):
        """Test updating a non-existent user."""
        result = UserService.update_user(999, {'first_name': 'Test'})
        self.assertIsNone(result)

    def test_delete_user_existing(self):
        """Test deleting an existing user."""
        user = UserService.create_user(self.user_data)
        success = UserService.delete_user(user.id)
        self.assertTrue(success)
        
        # Verify user is deleted
        self.assertIsNone(UserService.get_user_by_id(user.id))

    def test_delete_user_nonexistent(self):
        """Test deleting a non-existent user."""
        success = UserService.delete_user(999)
        self.assertFalse(success)

    def test_deactivate_user(self):
        """Test deactivating a user."""
        user = UserService.create_user(self.user_data)
        deactivated_user = UserService.deactivate_user(user.id)
        
        self.assertFalse(deactivated_user.is_active)

    def test_activate_user(self):
        """Test activating a user."""
        user_data = self.user_data.copy()
        user_data['is_active'] = False
        user = CustomUser.objects.create(**user_data)
        
        activated_user = UserService.activate_user(user.id)
        self.assertTrue(activated_user.is_active)

    def test_get_user_statistics(self):
        """Test getting user statistics."""
        # Create test users
        UserService.create_user(self.user_data)
        
        inactive_data = self.user_data.copy()
        inactive_data.update({
            'username': 'inactive',
            'email': 'inactive@example.com',
            'is_active': False
        })
        CustomUser.objects.create(**inactive_data)

        stats = UserService.get_user_statistics()
        self.assertEqual(stats['total_users'], 2)
        self.assertEqual(stats['active_users'], 1)
        self.assertEqual(stats['inactive_users'], 1)


class UserSerializerTestCase(TestCase):
    """Test cases for User serializers."""

    def setUp(self):
        """Set up test data for serializer tests."""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        }

    def test_user_serializer_valid_data(self):
        """Test UserSerializer with valid data."""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_user_serializer_password_mismatch(self):
        """Test UserSerializer with password mismatch."""
        data = self.user_data.copy()
        data['confirm_password'] = 'different'
        
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Passwords do not match', str(serializer.errors))

    def test_user_serializer_invalid_username(self):
        """Test UserSerializer with invalid username."""
        data = self.user_data.copy()
        data['username'] = 'ab'  # Too short
        
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_user_list_serializer(self):
        """Test UserListSerializer."""
        user = CustomUser.objects.create(
            username='listuser',
            email='list@example.com',
            first_name='List',
            last_name='User'
        )
        
        serializer = UserListSerializer(user)
        data = serializer.data
        
        self.assertEqual(data['username'], 'listuser')
        self.assertEqual(data['full_name'], 'List User')
        self.assertIn('date_joined', data)


class UserControllerTestCase(TestCase):
    """Test cases for UserController API endpoints."""

    def setUp(self):
        """Set up test client and data for API tests."""
        self.client = APIClient()
        self.user_data = {
            'username': 'apiuser',
            'email': 'api@example.com',
            'first_name': 'API',
            'last_name': 'User',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        }

    def test_create_user_api(self):
        """Test creating a user via API."""
        response = self.client.post('/api/users/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['username'], 'apiuser')

    def test_create_user_api_invalid_data(self):
        """Test creating a user with invalid data via API."""
        invalid_data = self.user_data.copy()
        del invalid_data['username']
        
        response = self.client.post('/api/users/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_list_users_api(self):
        """Test listing users via API."""
        CustomUser.objects.create(
            username='listuser1',
            email='list1@example.com',
            first_name='List',
            last_name='User1'
        )
        CustomUser.objects.create(
            username='listuser2',
            email='list2@example.com',
            first_name='List',
            last_name='User2'
        )

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['count'], 2)

    def test_retrieve_user_api(self):
        """Test retrieving a specific user via API."""
        user = CustomUser.objects.create(
            username='retrieveuser',
            email='retrieve@example.com',
            first_name='Retrieve',
            last_name='User'
        )

        response = self.client.get(f'/api/users/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['username'], 'retrieveuser')

    def test_retrieve_user_api_not_found(self):
        """Test retrieving a non-existent user via API."""
        response = self.client.get('/api/users/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['success'])

    def test_update_user_api(self):
        """Test updating a user via API."""
        user = CustomUser.objects.create(
            username='updateuser',
            email='update@example.com',
            first_name='Update',
            last_name='User'
        )

        update_data = {
            'username': 'updateuser',
            'email': 'update@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }

        response = self.client.put(f'/api/users/{user.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['first_name'], 'Updated')

    def test_partial_update_user_api(self):
        """Test partially updating a user via API."""
        user = CustomUser.objects.create(
            username='patchuser',
            email='patch@example.com',
            first_name='Patch',
            last_name='User'
        )

        patch_data = {'first_name': 'Patched'}

        response = self.client.patch(f'/api/users/{user.id}/', patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['first_name'], 'Patched')

    def test_delete_user_api(self):
        """Test deleting a user via API."""
        user = CustomUser.objects.create(
            username='deleteuser',
            email='delete@example.com',
            first_name='Delete',
            last_name='User'
        )

        response = self.client.delete(f'/api/users/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(response.data['success'])

    def test_deactivate_user_api(self):
        """Test deactivating a user via API."""
        user = CustomUser.objects.create(
            username='deactivateuser',
            email='deactivate@example.com',
            first_name='Deactivate',
            last_name='User'
        )

        response = self.client.post(f'/api/users/{user.id}/deactivate/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertFalse(response.data['data']['is_active'])

    def test_activate_user_api(self):
        """Test activating a user via API."""
        user = CustomUser.objects.create(
            username='activateuser',
            email='activate@example.com',
            first_name='Activate',
            last_name='User',
            is_active=False
        )

        response = self.client.post(f'/api/users/{user.id}/activate/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertTrue(response.data['data']['is_active'])

    def test_user_statistics_api(self):
        """Test getting user statistics via API."""
        CustomUser.objects.create(
            username='statsuser1',
            email='stats1@example.com',
            first_name='Stats',
            last_name='User1'
        )
        CustomUser.objects.create(
            username='statsuser2',
            email='stats2@example.com',
            first_name='Stats',
            last_name='User2',
            is_active=False
        )

        response = self.client.get('/api/users/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['total_users'], 2)
        self.assertEqual(response.data['data']['active_users'], 1)
        self.assertEqual(response.data['data']['inactive_users'], 1)

    def test_search_users_api(self):
        """Test searching users via API."""
        CustomUser.objects.create(
            username='searchuser',
            email='search@example.com',
            first_name='Search',
            last_name='User'
        )

        response = self.client.get('/api/users/?search=Search')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['count'], 1)
