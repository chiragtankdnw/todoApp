# User Management API Documentation

This document describes the complete User management system with full CRUD operations implemented in the Django todo app.

## Components Overview

### 1. User Model (`todo/models.py`)
- **Fields**: username, email, first_name, last_name, is_active, date_joined, last_login, profile_picture, bio
- **Methods**: `__str__()`, `get_full_name()`, `get_short_name()`
- **Validation**: Unique username and email, email format validation

### 2. UserService (`todo/services.py`)
- Business logic layer for User operations
- Handles complex operations and validations
- Transaction management for data integrity

### 3. UserController (`todo/views.py`)
- REST API endpoints for User management
- Error handling and response formatting
- Custom actions for activate/deactivate users

### 4. UserSerializer (`todo/serializers.py`)
- Data validation and serialization
- Password confirmation validation
- Different serializers for different use cases

## API Endpoints

### Base URL: `http://127.0.0.1:8000/api/users/`

### 1. List Users
**GET** `/api/users/`

**Query Parameters:**
- `active` (boolean): Filter by active status (default: true)
- `search` (string): Search in username, email, first_name, last_name

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
            "is_active": true,
            "date_joined": "2025-09-08T21:30:00Z"
        }
    ],
    "count": 1
}
```

### 2. Create User
**POST** `/api/users/`

**Request Body:**
```json
{
    "username": "new_user",
    "email": "user@example.com",
    "first_name": "New",
    "last_name": "User",
    "password": "secure123",
    "confirm_password": "secure123",
    "profile_picture": "https://example.com/avatar.jpg",
    "bio": "User biography"
}
```

**Response:**
```json
{
    "success": true,
    "message": "User created successfully",
    "data": {
        "id": 2,
        "username": "new_user",
        "email": "user@example.com",
        "first_name": "New",
        "last_name": "User",
        "full_name": "New User",
        "is_active": true,
        "date_joined": "2025-09-08T21:35:00Z",
        "profile_picture": "https://example.com/avatar.jpg",
        "bio": "User biography"
    }
}
```

### 3. Retrieve User
**GET** `/api/users/{id}/`

**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "is_active": true,
        "date_joined": "2025-09-08T21:30:00Z",
        "last_login": null,
        "profile_picture": null,
        "bio": ""
    }
}
```

### 4. Update User (Full)
**PUT** `/api/users/{id}/`

**Request Body:**
```json
{
    "username": "john_doe_updated",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "profile_picture": "https://example.com/new-avatar.jpg",
    "bio": "Updated biography"
}
```

### 5. Update User (Partial)
**PATCH** `/api/users/{id}/`

**Request Body:**
```json
{
    "first_name": "Johnny",
    "bio": "Partially updated bio"
}
```

### 6. Delete User
**DELETE** `/api/users/{id}/`

**Response:**
```json
{
    "success": true,
    "message": "User deleted successfully"
}
```

### 7. Deactivate User
**POST** `/api/users/{id}/deactivate/`

**Response:**
```json
{
    "success": true,
    "message": "User deactivated successfully",
    "data": {
        "id": 1,
        "username": "john_doe",
        "is_active": false,
        ...
    }
}
```

### 8. Activate User
**POST** `/api/users/{id}/activate/`

**Response:**
```json
{
    "success": true,
    "message": "User activated successfully",
    "data": {
        "id": 1,
        "username": "john_doe",
        "is_active": true,
        ...
    }
}
```

### 9. User Statistics
**GET** `/api/users/statistics/`

**Response:**
```json
{
    "success": true,
    "data": {
        "total_users": 10,
        "active_users": 8,
        "inactive_users": 2
    }
}
```

### 10. Search Users
**GET** `/api/users/?search=john`

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
            "is_active": true,
            "date_joined": "2025-09-08T21:30:00Z"
        }
    ],
    "count": 1
}
```

## Error Responses

### Validation Error (400)
```json
{
    "success": false,
    "errors": {
        "username": ["This field is required."],
        "email": ["Enter a valid email address."]
    }
}
```

### Not Found Error (404)
```json
{
    "success": false,
    "error": "User not found"
}
```

### Server Error (500)
```json
{
    "success": false,
    "error": "Internal server error message"
}
```

## Testing

### Run All Tests
```bash
python manage.py test todo
```

### Run User System Tests Only
```bash
python manage.py test todo.test_user_system
```

### Run Calculator Tests Only
```bash
python manage.py test todo.tests
```

## Test Coverage

- **70 total tests** covering all functionality
- **42 User management tests** (models, services, serializers, API endpoints)
- **28 Calculator utility tests** (comprehensive coverage of all operations)

### User Test Categories:
1. **Model Tests** (7 tests): User creation, validation, methods
2. **Service Tests** (20 tests): Business logic, CRUD operations, error handling
3. **Serializer Tests** (4 tests): Data validation, serialization
4. **API Tests** (11 tests): Complete CRUD endpoints, custom actions

## Usage Examples

### Testing with curl:

```bash
# Create a user
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "test123",
    "confirm_password": "test123"
  }'

# List all users
curl http://127.0.0.1:8000/api/users/

# Get user by ID
curl http://127.0.0.1:8000/api/users/1/

# Search users
curl "http://127.0.0.1:8000/api/users/?search=test"

# Get statistics
curl http://127.0.0.1:8000/api/users/statistics/
```

## Architecture Benefits

1. **Separation of Concerns**: Clear separation between models, services, and controllers
2. **Reusability**: Service layer can be used by different controllers or management commands
3. **Testability**: Each layer is independently testable
4. **Maintainability**: Business logic is centralized in services
5. **Scalability**: Easy to extend with new features
6. **Error Handling**: Comprehensive error handling at all levels
7. **Validation**: Multiple layers of validation (model, serializer, service)

This implementation follows Django and REST API best practices for production-ready applications.
