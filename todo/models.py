from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone
# Create your models here.


class CustomUser(models.Model):
    """
    Custom User model for managing user accounts in the todo application.
    
    This model provides user functionality without conflicts with Django's built-in User model.
    
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
    bio = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'todo_customuser'
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        ordering = ['-date_joined']

    def __str__(self):
        """Return the username as string representation."""
        return self.username

    def get_full_name(self):
        """Return the user's full name."""
        return ' '.join(part for part in [self.first_name, self.last_name] if part).strip()

    def get_short_name(self):
        """Return the user's first name."""
        return self.first_name


class Todo(models.Model):

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


class BlogPostSummary(models.Model):
    """
    Model for storing blog post summaries and metadata.
    
    Attributes:
        title (CharField): Title of the blog post. Maximum 300 characters.
        url (URLField): Source URL of the blog post.
        date_published (DateField): Publication date of the blog post.
        summary (TextField): High-level technical summary of the blog post.
        tags (CharField): Comma-separated tags for categorization.
        location_timezone (CharField): Timezone information for the post.
        created_at (DateTimeField): Timestamp when summary was added.
        updated_at (DateTimeField): Timestamp when summary was last updated.
    """
    title = models.CharField(max_length=300)
    url = models.URLField(max_length=500)
    date_published = models.DateField()
    summary = models.TextField()
    tags = models.CharField(max_length=200, blank=True, null=True)
    location_timezone = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'todo_blogpostsummary'
        verbose_name = 'Blog Post Summary'
        verbose_name_plural = 'Blog Post Summaries'
        ordering = ['-date_published', '-created_at']

    def __str__(self):
        """Return the title as string representation."""
        return self.title
