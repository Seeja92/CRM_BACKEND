from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company


class CompanyOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class CompanySerializer(serializers.ModelSerializer):
    company_owner = CompanyOwnerSerializer(many=True, read_only=True)
    company_owner_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        source='company_owner'
    )
    created_at = serializers.DateTimeField(read_only=True, format='%b %d, %Y %I:%M %p')

    class Meta:
        model = Company
        fields = [
            'id',
            'domain_name',
            'company_name',
            'company_owner',
            'company_owner_ids',
            'industry',
            'type',
            'city',
            'country',
            'no_of_employees',
            'annual_revenue',
            'email',
            'phone_number',
            'created_at',
        ]

    def create(self, validated_data):
        owners = validated_data.pop('company_owner', [])
        company = Company.objects.create(**validated_data)
        company.company_owner.set(owners)
        return company

    def update(self, instance, validated_data):
        owners = validated_data.pop('company_owner', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if owners is not None:
            instance.company_owner.set(owners)
        return instance


class CompanyListSerializer(serializers.ModelSerializer):
    company_owner = CompanyOwnerSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format='%b %d, %Y %I:%M %p')

    class Meta:
        model = Company
        fields = [
            'id',
            'company_name',
            'company_owner',
            'phone_number',
            'industry',
            'city',
            'country',
            'created_at',
        ]