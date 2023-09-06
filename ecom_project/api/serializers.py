from rest_framework import serializers
from .models import UserProfile
from rest_framework import serializers
from .models import Product

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']
        extra_kwargs = {"password": {"write_only": True}}

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']

  

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
