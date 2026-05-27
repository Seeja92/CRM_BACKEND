from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display  = ['id', 'first_name', 'last_name', 'email', 'phone', 'status', 'created_date']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_filter   = ['status']