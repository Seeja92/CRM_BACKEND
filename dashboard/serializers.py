"""
dashboard/serializers.py
────────────────────────
Serializers for all dashboard API response shapes.
"""

from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    total_leads      = serializers.IntegerField()
    active_deals     = serializers.IntegerField()
    closed_deals     = serializers.IntegerField()
    monthly_revenue  = serializers.FloatField()
    total_companies  = serializers.IntegerField()


class ConversionStageSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.IntegerField()   # 0–100
    color = serializers.CharField()      # hex color


class SalesDataPointSerializer(serializers.Serializer):
    month = serializers.CharField()      # "Jan"…"Dec" or "2024"
    value = serializers.FloatField()


class TeamMemberSerializer(serializers.Serializer):
    name         = serializers.CharField()
    active_deals = serializers.IntegerField()
    closed_deals = serializers.IntegerField()
    revenue      = serializers.CharField()   # pre-formatted "$12,000"
    change       = serializers.CharField()   # "+3.4%" or "-0.1%"
    positive     = serializers.BooleanField()