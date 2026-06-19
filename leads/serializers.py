# from rest_framework import serializers
# from .models import Lead

# class LeadSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()

#     class Meta:
#         model = Lead
#         fields = [
#             'id', 'name', 'first_name', 'last_name',
#             'email', 'phone', 'company_name','company',
#             'job_title','contact_owner', 'status','city', 'created_date',
#         ]

#     def get_name(self, obj):
#         return f"{obj.first_name} {obj.last_name}"

from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    contact_owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            'id',
            'name',
            'first_name',
            'last_name',
            'email',
            'phone',
            'company_name',
            'company',
            'job_title',
            'contact_owner',
            'contact_owner_name',
            'status',
            'city',
            'created_date',
        ]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_contact_owner_name(self, obj):
        if obj.contact_owner:
            return f"{obj.contact_owner.first_name} {obj.contact_owner.last_name}".strip()
        return None