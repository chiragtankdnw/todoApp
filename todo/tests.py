from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Todo
from datetime import date

class TodoModelTest(TestCase):
    def test_todo_creation_with_dates(self):
        """Test creating a todo with start and end dates"""
        todo = Todo.objects.create(
            title="Test Todo",
            description="Test description",
            start_date=date(2023, 12, 1),
            end_date=date(2023, 12, 15)
        )
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.start_date, date(2023, 12, 1))
        self.assertEqual(todo.end_date, date(2023, 12, 15))
        self.assertFalse(todo.completed)

    def test_todo_creation_without_dates(self):
        """Test creating a todo without dates (should be allowed)"""
        todo = Todo.objects.create(
            title="No Dates Todo",
            description="Test description"
        )
        self.assertEqual(todo.title, "No Dates Todo")
        self.assertIsNone(todo.start_date)
        self.assertIsNone(todo.end_date)

    def test_todo_validation_end_before_start(self):
        """Test that end date cannot be before start date"""
        todo = Todo(
            title="Invalid Todo",
            description="Test description",
            start_date=date(2023, 12, 15),
            end_date=date(2023, 12, 1)
        )
        with self.assertRaises(ValidationError):
            todo.full_clean()

    def test_todo_validation_valid_dates(self):
        """Test that valid date ranges pass validation"""
        todo = Todo(
            title="Valid Todo",
            description="Test description",
            start_date=date(2023, 12, 1),
            end_date=date(2023, 12, 15)
        )
        try:
            todo.full_clean()
        except ValidationError:
            self.fail("Valid date range should not raise ValidationError")


class TodoAPITest(APITestCase):
    def test_create_todo_with_dates(self):
        """Test creating todo via API with dates"""
        data = {
            'title': 'API Test Todo',
            'description': 'Test via API',
            'start_date': '2023-12-01',
            'end_date': '2023-12-15'
        }
        response = self.client.post('/api/todos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'API Test Todo')
        self.assertEqual(response.data['start_date'], '2023-12-01')
        self.assertEqual(response.data['end_date'], '2023-12-15')

    def test_create_todo_without_dates(self):
        """Test creating todo via API without dates"""
        data = {
            'title': 'No Dates API Todo',
            'description': 'Test via API without dates'
        }
        response = self.client.post('/api/todos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'No Dates API Todo')
        self.assertIsNone(response.data['start_date'])
        self.assertIsNone(response.data['end_date'])

    def test_create_todo_invalid_dates(self):
        """Test API validation for invalid date range"""
        data = {
            'title': 'Invalid API Todo',
            'description': 'Test invalid dates',
            'start_date': '2023-12-15',
            'end_date': '2023-12-01'
        }
        response = self.client.post('/api/todos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('End date cannot be before start date', str(response.data))

    def test_get_todos_includes_dates(self):
        """Test that GET request includes date fields"""
        Todo.objects.create(
            title="Test Todo",
            description="Test",
            start_date=date(2023, 12, 1),
            end_date=date(2023, 12, 15)
        )
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        todo_data = response.data[0]
        self.assertIn('start_date', todo_data)
        self.assertIn('end_date', todo_data)
        self.assertEqual(todo_data['start_date'], '2023-12-01')
        self.assertEqual(todo_data['end_date'], '2023-12-15')
