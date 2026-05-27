
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile

class RegisterSerializer(serializers.Serializer):
    first_name        = serializers.CharField()
    last_name         = serializers.CharField()
    email             = serializers.EmailField()
    phone_number      = serializers.CharField()
    company_name      = serializers.CharField()
    industry_type     = serializers.CharField()
    country_or_region = serializers.CharField()
    role              = serializers.CharField()
    password          = serializers.CharField(write_only=True)
    confirm_password  = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    # FIXED: This method must be indented to be inside the class
    def create(self, validated_data):
        # 1. Remove confirm_password as it's not needed for the User model
        validated_data.pop('confirm_password')
        
        # 2. Extract profile fields to separate them from the User fields
        profile_data = {
            'phone_number': validated_data.pop('phone_number'),
            'company_name': validated_data.pop('company_name'),
            'industry_type': validated_data.pop('industry_type'),
            'country_or_region': validated_data.pop('country_or_region'),
            'role': validated_data.pop('role'),
        }

        # 3. Create the User (setting username = email for authentication)
        user = User.objects.create_user(
            username=validated_data['email'], 
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )

        # 4. Create the UserProfile linked to the new user
        UserProfile.objects.create(user=user, **profile_data)
        
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # We use username=email because that is how the user was created
            user = authenticate(username=email, password=password)

            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        data['user'] = user
        return data