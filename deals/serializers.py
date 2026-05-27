
from rest_framework import serializers
from .models import Deal, DealActivity
from leads.serializers import LeadSerializer  # ← import your Lead serializer

class DealSerializer(serializers.ModelSerializer):
    associated_lead = LeadSerializer(read_only=True)                    # ← nested object for GET
    associated_lead_id = serializers.PrimaryKeyRelatedField(            # ← accepts ID for POST/PATCH
        queryset=__import__('leads.models', fromlist=['Lead']).Lead.objects.all(),
        source='associated_lead',
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model  = Deal
        fields = [
            'id', 'deal_name', 'deal_stage', 'close_date',
            'deal_owner', 'amount', 'priority',
            'associated_lead',      # ← returns nested { id, first_name, last_name, ... }
            'associated_lead_id',   # ← accepts integer ID on create/update
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class DealActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = DealActivity
        fields = ['id', 'deal', 'message', 'activity_type', 'created_at']
        read_only_fields = ['id', 'created_at']
