# Need serializers to convert model instances to JSON so that the frontend
# can work with the received data easily.

# We will create a todo/serializers.py file:

from rest_framework import serializers
from .models import Todo

#  Specify the model to work with and the fields we want to be converted to JSON.
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed', 'start_date', 'end_date')
        
    def validate(self, data):
        """
        Custom validation to ensure end_date is not before start_date.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("End date cannot be before start date.")
            
        return data
