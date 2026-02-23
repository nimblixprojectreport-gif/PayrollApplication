from rest_framework import serializers
from .models import User

class UserListDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = User
        fields = [
            'id', 'company', 'company_name', 'username', 'email', 
            'mobile', 'is_active', 'last_login', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'last_login', 'created_at', 'updated_at']

class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'company', 'username', 'email',
            'mobile', 'password_hash', 'is_active'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }
