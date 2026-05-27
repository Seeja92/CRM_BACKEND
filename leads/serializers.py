from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'first_name', 'last_name',
            'email', 'phone', 'company_name',
            'job_title','contact_owner', 'status', 'created_date',
        ]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"