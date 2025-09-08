from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from .serializers import TodoSerializer, UserSerializer, UserListSerializer
from .models import Todo, CustomUser
from .services import UserService
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound
import os

# Constants for error messages
USER_NOT_FOUND_ERROR = 'User not found'
USER_CREATED_SUCCESS = 'User created successfully'
USER_UPDATED_SUCCESS = 'User updated successfully'
USER_DELETED_SUCCESS = 'User deleted successfully'
USER_ACTIVATED_SUCCESS = 'User activated successfully'
USER_DEACTIVATED_SUCCESS = 'User deactivated successfully'

# The viewsets base class provides the implementation for CRUD operations by default,
# what we had to do was specify the serializer class and the query set.


class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


class UserController(viewsets.ModelViewSet):
    """
    API Controller for User management with full CRUD operations.
    
    This viewset provides complete REST API endpoints for User entities:
    - GET /api/users/ - List all users
    - POST /api/users/ - Create a new user
    - GET /api/users/{id}/ - Retrieve a specific user
    - PUT /api/users/{id}/ - Update a specific user (full update)
    - PATCH /api/users/{id}/ - Partially update a specific user
    - DELETE /api/users/{id}/ - Delete a specific user
    
    Additional custom endpoints:
    - POST /api/users/{id}/deactivate/ - Deactivate a user
    - POST /api/users/{id}/activate/ - Activate a user
    - GET /api/users/search/?q={query} - Search users
    - GET /api/users/statistics/ - Get user statistics
    """
    
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        Uses UserListSerializer for list view and UserSerializer for others.
        """
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer

    def list(self, request):
        """
        GET /api/users/
        List all users with optional filtering.
        
        Query Parameters:
            - active: Filter by active status (true/false)
            - search: Search query for username, email, or name
        """
        try:
            # Get query parameters
            active_only = request.query_params.get('active', 'true').lower() == 'true'
            search_query = request.query_params.get('search', '').strip()

            if search_query:
                users = UserService.search_users(search_query)
            else:
                users = UserService.get_all_users(active_only=active_only)

            serializer = self.get_serializer(users, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'count': len(serializer.data)
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """
        POST /api/users/
        Create a new user.
        
        Request Body:
            {
                "username": "string",
                "email": "string",
                "first_name": "string",
                "last_name": "string",
                "password": "string",
                "confirm_password": "string",
                "profile_picture": "string (optional)",
                "bio": "string (optional)"
            }
        """
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = UserService.create_user(serializer.validated_data)
                response_serializer = UserSerializer(user)
                return Response({
                    'success': True,
                    'message': USER_CREATED_SUCCESS,
                    'data': response_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """
        GET /api/users/{id}/
        Retrieve a specific user by ID.
        """
        try:
            user = UserService.get_user_by_id(pk)
            if not user:
                return Response({
                    'success': False,
                    'error': USER_NOT_FOUND_ERROR
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(user)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """
        PUT /api/users/{id}/
        Update a user (full update).
        """
        try:
            user = UserService.get_user_by_id(pk)
            if not user:
                return Response({
                    'success': False,
                    'error': USER_NOT_FOUND_ERROR
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(user, data=request.data)
            if serializer.is_valid():
                updated_user = UserService.update_user(pk, serializer.validated_data)
                response_serializer = UserSerializer(updated_user)
                return Response({
                    'success': True,
                    'message': USER_UPDATED_SUCCESS,
                    'data': response_serializer.data
                })
            else:
                return Response({
                    'success': False,
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        """
        PATCH /api/users/{id}/
        Partially update a user.
        """
        try:
            user = UserService.get_user_by_id(pk)
            if not user:
                return Response({
                    'success': False,
                    'error': USER_NOT_FOUND_ERROR
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                updated_user = UserService.update_user(pk, serializer.validated_data)
                response_serializer = UserSerializer(updated_user)
                return Response({
                    'success': True,
                    'message': USER_UPDATED_SUCCESS,
                    'data': response_serializer.data
                })
            else:
                return Response({
                    'success': False,
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """
        DELETE /api/users/{id}/
        Delete a user.
        """
        try:
            success = UserService.delete_user(pk)
            if not success:
                return Response({
                    'success': False,
                    'error': USER_NOT_FOUND_ERROR
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'success': True,
                'message': USER_DELETED_SUCCESS
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        POST /api/users/{id}/deactivate/
        Deactivate a user account.
        """
        try:
            user = UserService.deactivate_user(pk)
            if not user:
                return Response({
                    'success': False,
                    'error': USER_NOT_FOUND_ERROR
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)
            return Response({
                'success': True,
                'message': USER_DEACTIVATED_SUCCESS,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        POST /api/users/{id}/activate/
        Activate a user account.
        """
        try:
            user = UserService.activate_user(pk)
            if not user:
                return Response({
                    'success': False,
                    'error': USER_NOT_FOUND_ERROR
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)
            return Response({
                'success': True,
                'message': USER_ACTIVATED_SUCCESS,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        GET /api/users/statistics/
        Get user statistics.
        """
        try:
            stats = UserService.get_user_statistics()
            return Response({
                'success': True,
                'data': stats
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Assets(View):

    def get(self, _request, filename):
        path = os.path.join(os.path.dirname(__file__), 'static', filename)

        if os.path.isfile(path):
            with open(path, 'rb') as file:
                return HttpResponse(file.read(), content_type='application/javascript')
        else:
            return HttpResponseNotFound()
