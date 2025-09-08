"""
Service layer for User management operations.

This module contains business logic and data access operations for User entities.
Services act as an intermediary between views (controllers) and models,
providing reusable business logic and complex operations.
"""

from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import CustomUser
from typing import List, Dict, Optional, Any


class UserService:
    """
    Service class for CustomUser-related business operations.
    
    This service handles all business logic related to user management,
    including CRUD operations, validation, and complex queries.
    """

    @staticmethod
    def get_all_users(active_only: bool = True) -> List[CustomUser]:
        """
        Retrieve all users from the database.
        
        Args:
            active_only (bool): If True, return only active users. Defaults to True.
            
        Returns:
            List[CustomUser]: List of CustomUser instances
        """
        queryset = CustomUser.objects.all()
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('-date_joined')

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[CustomUser]:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id (int): The ID of the user to retrieve
            
        Returns:
            Optional[CustomUser]: CustomUser instance if found, None otherwise
        """
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_username(username: str) -> Optional[CustomUser]:
        """
        Retrieve a user by their username.
        
        Args:
            username (str): The username to search for
            
        Returns:
            Optional[CustomUser]: CustomUser instance if found, None otherwise
        """
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[CustomUser]:
        """
        Retrieve a user by their email address.
        
        Args:
            email (str): The email address to search for
            
        Returns:
            Optional[CustomUser]: CustomUser instance if found, None otherwise
        """
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def create_user(user_data: Dict[str, Any]) -> CustomUser:
        """
        Create a new user with the provided data.
        
        Args:
            user_data (Dict[str, Any]): Dictionary containing user information
            
        Returns:
            CustomUser: The created CustomUser instance
            
        Raises:
            ValidationError: If user data is invalid
        """
        # Validate required fields
        required_fields = ['username', 'email', 'first_name', 'last_name']
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                raise ValidationError(f"{field} is required")

        # Check if username already exists
        if CustomUser.objects.filter(username=user_data['username']).exists():
            raise ValidationError("Username already exists")

        # Check if email already exists
        if CustomUser.objects.filter(email=user_data['email']).exists():
            raise ValidationError("Email already exists")

        # Remove fields that are not part of the User model
        clean_data = user_data.copy()
        clean_data.pop('password', None)
        clean_data.pop('confirm_password', None)

        # Create the user
        user = CustomUser.objects.create(**clean_data)
        return user

    @staticmethod
    @transaction.atomic
    def update_user(user_id: int, user_data: Dict[str, Any]) -> Optional[CustomUser]:
        """
        Update an existing user with the provided data.
        
        Args:
            user_id (int): The ID of the user to update
            user_data (Dict[str, Any]): Dictionary containing updated user information
            
        Returns:
            Optional[CustomUser]: The updated CustomUser instance if found, None otherwise
            
        Raises:
            ValidationError: If user data is invalid
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            return None

        # Check username uniqueness if being updated
        if 'username' in user_data and user_data['username'] != user.username:
            if CustomUser.objects.filter(username=user_data['username']).exists():
                raise ValidationError("Username already exists")

        # Check email uniqueness if being updated
        if 'email' in user_data and user_data['email'] != user.email:
            if CustomUser.objects.filter(email=user_data['email']).exists():
                raise ValidationError("Email already exists")

        # Remove fields that are not part of the User model
        clean_data = user_data.copy()
        clean_data.pop('password', None)
        clean_data.pop('confirm_password', None)

        # Update user fields
        for field, value in clean_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        user.save()
        return user

    @staticmethod
    @transaction.atomic
    def delete_user(user_id: int) -> bool:
        """
        Delete a user by their ID.
        
        Args:
            user_id (int): The ID of the user to delete
            
        Returns:
            bool: True if user was deleted, False if user was not found
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            return False

        user.delete()
        return True

    @staticmethod
    @transaction.atomic
    def deactivate_user(user_id: int) -> Optional[CustomUser]:
        """
        Deactivate a user instead of deleting them.
        
        Args:
            user_id (int): The ID of the user to deactivate
            
        Returns:
            Optional[CustomUser]: The deactivated CustomUser instance if found, None otherwise
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            return None

        user.is_active = False
        user.save()
        return user

    @staticmethod
    @transaction.atomic
    def activate_user(user_id: int) -> Optional[CustomUser]:
        """
        Activate a deactivated user.
        
        Args:
            user_id (int): The ID of the user to activate
            
        Returns:
            Optional[CustomUser]: The activated CustomUser instance if found, None otherwise
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            return None

        user.is_active = True
        user.save()
        return user

    @staticmethod
    def search_users(query: str) -> List[CustomUser]:
        """
        Search for users by username, email, first name, or last name.
        
        Args:
            query (str): The search query
            
        Returns:
            List[CustomUser]: List of matching CustomUser instances
        """
        return CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).filter(is_active=True).order_by('-date_joined')

    @staticmethod
    def get_user_statistics() -> Dict[str, int]:
        """
        Get statistics about users in the system.
        
        Returns:
            Dict[str, int]: Dictionary containing user statistics
        """
        total_users = CustomUser.objects.count()
        active_users = CustomUser.objects.filter(is_active=True).count()
        inactive_users = total_users - active_users
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users
        }

    @staticmethod
    @transaction.atomic
    def update_last_login(user_id: int) -> Optional[CustomUser]:
        """
        Update the last login timestamp for a user.
        
        Args:
            user_id (int): The ID of the user
            
        Returns:
            Optional[CustomUser]: The updated CustomUser instance if found, None otherwise
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            return None

        user.last_login = timezone.now()
        user.save()
        return user
