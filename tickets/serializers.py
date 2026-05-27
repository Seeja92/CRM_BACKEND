

from rest_framework import serializers
from .models import Ticket
from deals.models import Deal
from companies.models import Company
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketSerializer(serializers.ModelSerializer):

    # ── Read-only display fields ──────────────────────────────────────────────
    company_name = serializers.CharField(
        source='company.company_name',
        read_only=True
    )

    owner_name = serializers.SerializerMethodField()

    associated_deal = serializers.SerializerMethodField()

    # ── Write-only FK fields ──────────────────────────────────────────────────
    deal_id = serializers.PrimaryKeyRelatedField(
        queryset=Deal.objects.all(),
        source='deal',
        write_only=True,
        allow_null=True,
        required=False
    )
    ticket_owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='ticket_owner',
        write_only=True,
        allow_null=True,
        required=False
    )
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source='company',
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Ticket
        fields = [
            'id',
            'ticket_name',
            'status',
            'source',
            'priority',
            # ── read-only ──
            'company_name',
            'owner_name',
            'associated_deal',
            # ── write-only ──
            'deal_id',
            'ticket_owner_id',
            'company_id',
            'created_at',
            'updated_at',
        ]

    def get_owner_name(self, obj):
        if not obj.ticket_owner:
            return None
        # handles custom User model with .name field
        name = getattr(obj.ticket_owner, 'name', None)
        if name:
            return name
        # fallback for default Django User
        first = getattr(obj.ticket_owner, 'first_name', '')
        last  = getattr(obj.ticket_owner, 'last_name', '')
        return f"{first} {last}".strip() or obj.ticket_owner.username

    def get_associated_deal(self, obj):
        deal = obj.deal
        if not deal:
            return None

        lead = getattr(deal, 'associated_lead', None)
        lead_data = None
        if lead:
            lead_data = {
                'id':           lead.id,
                'first_name':   lead.first_name,
                'last_name':    lead.last_name,
                'email':        lead.email,
                'phone_number': getattr(lead, 'phone', None) or getattr(lead, 'phone_number', None),
            }

        return {
            'id':              deal.id,
            'deal_name':       deal.deal_name,
            'associated_lead': lead_data,
        }