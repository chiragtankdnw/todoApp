from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils import timezone
# Create your models here.


class User(models.Model):
    """
    Custom User model for managing user accounts in the todo application.
    
    This model extends the basic user functionality with additional fields
    for profile information and account management.
    
    Attributes:
        username (CharField): Unique username for login. Maximum 150 characters.
        email (EmailField): User's email address. Must be unique across all users.
        first_name (CharField): User's first name. Maximum 30 characters.
        last_name (CharField): User's last name. Maximum 30 characters.
        is_active (BooleanField): Whether the user account is active. Defaults to True.
        date_joined (DateTimeField): Timestamp when the user account was created.
        last_login (DateTimeField): Timestamp of the user's last login (nullable).
        profile_picture (URLField): Optional URL to user's profile picture.
        bio (TextField): Optional biography/description of the user.
    
    Methods:
        __str__(): Returns the username as string representation.
        get_full_name(): Returns the user's full name (first + last name).
        get_short_name(): Returns the user's first name.
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    bio = models.TextField(blank=True)

    class Meta:
        db_table = 'todo_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        """Return the username as string representation."""
        return self.username

    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the user's first name."""
        return self.first_name


class Todo(models.Model):
    """
    Django model representing a Todo item in the task management system.
    
    This model stores individual todo tasks with their completion status and
    provides the core data structure for the todo application's CRUD operations.
    
    Attributes:
        title (CharField): The title/name of the todo item. Maximum length of 120 characters.
                          This field is required and serves as the primary identifier for the task.
        description (TextField): Detailed description of the todo item. Can contain unlimited text
                               to provide additional context or instructions for the task.
        completed (BooleanField): Boolean flag indicating whether the todo item has been completed.
                                Defaults to False when a new todo is created.
    
    Methods:
        __str__(): Returns the string representation of the todo item (the title).
    
    Usage:
        # Create a new todo
        todo = Todo.objects.create(
            title="Complete project documentation",
            description="Write comprehensive docs for the API endpoints"
        )
        
        # Mark as completed
        todo.completed = True
        todo.save()
    
    Database Schema:
        - id: Primary key (auto-generated)
        - title: VARCHAR(120) NOT NULL
        - description: TEXT NOT NULL
        - completed: BOOLEAN DEFAULT FALSE
    """
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        """
        Return string representation of the Todo instance.
        
        Returns:
            str: The title of the todo item, used for display purposes in Django admin,
                 shell, and anywhere the model instance needs to be represented as text.
        
        Example:
            >>> todo = Todo(title="Buy groceries")
            >>> str(todo)
            'Buy groceries'
        """
        return self.title
