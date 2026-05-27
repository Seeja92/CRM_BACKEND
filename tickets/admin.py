from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ['id', 'ticket_name', 'status', 'priority', 'source', 'ticket_owner', 'company', 'deal', 'created_at']
    list_filter   = ['status', 'priority', 'source']
    search_fields = ['ticket_name', 'ticket_owner__first_name', 'ticket_owner__last_name', 'company__company_name', 'deal__deal_name']