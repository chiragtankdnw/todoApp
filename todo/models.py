from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


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
        start_date (DateField): Optional start date for when the task should begin.
                               Can be null to allow tasks without specific start dates.
        end_date (DateField): Optional end date for when the task should be completed.
                             Can be null to allow tasks without specific deadlines.
    
    Methods:
        __str__(): Returns the string representation of the todo item (the title).
        clean(): Validates that end_date is not before start_date when both are provided.
    
    Usage:
        # Create a new todo
        todo = Todo.objects.create(
            title="Complete project documentation",
            description="Write comprehensive docs for the API endpoints",
            start_date="2023-01-01",
            end_date="2023-01-15"
        )
        
        # Mark as completed
        todo.completed = True
        todo.save()
    
    Database Schema:
        - id: Primary key (auto-generated)
        - title: VARCHAR(120) NOT NULL
        - description: TEXT NOT NULL
        - completed: BOOLEAN DEFAULT FALSE
        - start_date: DATE NULL
        - end_date: DATE NULL
    """
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True, help_text="Optional start date for the task")
    end_date = models.DateField(null=True, blank=True, help_text="Optional end date for the task")

    def clean(self):
        """
        Validates that end_date is not before start_date when both dates are provided.
        
        Raises:
            ValidationError: If end_date is before start_date
        """
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError('End date cannot be before start date.')

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
