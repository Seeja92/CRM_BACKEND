from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display  = ['company_name', 'industry', 'type', 'city', 'country', 'created_at']
    search_fields = ['company_name', 'domain_name', 'email']
    list_filter   = ['industry', 'type']