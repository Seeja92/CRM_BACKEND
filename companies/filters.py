import django_filters
from .models import Company

class CompanyFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    industry = django_filters.CharFilter(field_name='industry', lookup_expr='exact')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')
    lead_status = django_filters.CharFilter(method='filter_lead_status') 
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')  # ← change
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')    # ← change

    class Meta:
        model = Company
        fields = ['industry', 'city', 'country', 'date_from', 'date_to']

    def filter_search(self, queryset, name, value):
        return (
            queryset.filter(company_name__icontains=value) |
            queryset.filter(phone_number__icontains=value) |
            queryset.filter(city__icontains=value) |
            queryset.filter(country__icontains=value) |  
            queryset.filter(company_owner__first_name__icontains=value) |
            queryset.filter(company_owner__last_name__icontains=value)
        ).distinct()
    
    def filter_lead_status(self, queryset, name, value):  # ← add
        if value and value != 'All':
            return queryset.filter(
                leads__status=value   # ← through optional FK relationship
            ).distinct()
        return queryset