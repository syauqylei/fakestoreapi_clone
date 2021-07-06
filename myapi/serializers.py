from django.contrib.auth.models import User
from .models import Product
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=255, validators=[UniqueValidator(
        queryset=User.objects.all(), message='Email has been already used')])
    username = serializers.CharField(
        required=True, max_length=255, min_length=6, validators=[UniqueValidator(
            queryset=User.objects.all(), message='Username has been already used')])
    password = serializers.CharField(
        required=True, max_length=255, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'category', 'description', 'image']
