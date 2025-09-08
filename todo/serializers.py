# Need serializers to convert model instances to JSON so that the frontend
# can work with the received data easily.

# We will create a todo/serializers.py file:

from rest_framework import serializers
from .models import Todo, CustomUser

#  Specify the model to work with and the fields we want to be converted to JSON.
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model with full CRUD operations support.
    
    Handles serialization and deserialization of CustomUser instances for API endpoints.
    Includes validation for email uniqueness and username requirements.
    """
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'is_active', 'date_joined', 'last_login', 'profile_picture', 
            'bio', 'password', 'confirm_password', 'full_name'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
        }

    def get_full_name(self, obj):
        """Return the user's full name."""
        return obj.get_full_name()

    def validate_username(self, value):
        """Validate username requirements."""
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        if not value.isalnum() and '_' not in value:
            raise serializers.ValidationError("Username can only contain letters, numbers, and underscores.")
        return value

    def validate_email(self, value):
        """Validate email uniqueness on update."""
        if self.instance and self.instance.email != value:
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("A user with this email already exists.")
        elif not self.instance and CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, attrs):
        """Validate password confirmation if provided."""
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match.")
        elif password and not confirm_password:
            raise serializers.ValidationError("Password confirmation is required.")
        
        return attrs

    def create(self, validated_data):
        """Create a new user instance."""
        # Remove password confirmation from validated data
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)
        
        user = CustomUser.objects.create(**validated_data)
        
        # Note: In a real application, you might want to hash the password
        # For this example, we're storing it as plain text (not recommended for production)
        if password:
            # user.set_password(password)  # Use this for hashed passwords
            pass
        
        return user

    def update(self, instance, validated_data):
        """Update an existing user instance."""
        # Remove password confirmation from validated data
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            # instance.set_password(password)  # Use this for hashed passwords
            pass
        
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for user list views.
    Contains only essential fields for listing users.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'full_name', 'is_active', 'date_joined')

    def get_full_name(self, obj):
        """Return the user's full name."""
        return obj.get_full_name()
