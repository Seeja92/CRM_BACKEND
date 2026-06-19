
from rest_framework import serializers
from .models import Deal, DealActivity
from leads.models import Lead
from django.contrib.auth.models import User


class DealSerializer(serializers.ModelSerializer):

    deal_owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )
    # ← Nested lead object for reading
    associated_lead = serializers.SerializerMethodField()
    
    # ← Write-only field for accepting lead ID
    associated_lead_id = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(),
        source='associated_lead',
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Deal
        fields = [
            'id', 'deal_name', 'deal_stage', 'close_date',
            'deal_owner', 'amount', 'priority',
            'associated_lead',      # ← read (nested object)
            'associated_lead_id',   # ← write (accepts ID)
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_associated_lead(self, obj):
        if not obj.associated_lead:
            return None
        lead = obj.associated_lead
        return {
            'id':           lead.id,
            'first_name':   lead.first_name,
            'last_name':    lead.last_name,
            'email':        lead.email,
            'phone_number': getattr(lead, 'phone', None) or getattr(lead, 'phone_number', None),
            'city':         getattr(lead, 'city', None),  # ← add this
        }


class DealActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DealActivity
        fields = [
            'id', 'deal', 'message', 'activity_type',
            'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']