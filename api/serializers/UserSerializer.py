from rest_framework.serializers import ModelSerializer
from api.models import User
from django.db import transaction
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'email': {'read_only': True},
            'is_active': {'read_only': True},
        }


# class UserRegisterSerializer(ModelSerializer):

#     def create(self, validated_data):
#         user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'])
#         return user

    # class Meta:
    #     model = User
    #     exclude = ['last_login', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'user_permissions', 'groups']
    #     extra_kwargs = {
    #         'password': {'write_only': True},
    #     }


class UserRegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
                
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)

        name = validated_data.pop('name', None)

        with transaction.atomic():

            user = User.objects.filter(email=validated_data['email']).first()

            if not user:
                user = User.objects.create_user(**validated_data)

            if name:
                user.name = name

            user.save()

        return user
    
    class Meta:
        model = User
        exclude = ['last_login', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'user_permissions', 'groups']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }