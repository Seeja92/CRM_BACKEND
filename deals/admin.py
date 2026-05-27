from django.contrib import admin
from .models import Deal

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['id', 'deal_name', 'deal_stage', 'deal_owner', 'amount', 'priority', 'close_date']
    search_fields = ['deal_name', 'deal_owner']
    list_filter = ['deal_stage', 'priority']