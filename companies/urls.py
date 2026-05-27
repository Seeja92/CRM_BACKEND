from django.urls import path
from .views import (
    CompanyListCreateView,
    CompanyDetailView,
    CompanySearchView,
    import_companies
)

urlpatterns = [
    path('', CompanyListCreateView.as_view(), name='company-list-create'),
    path('import/', import_companies, name='import_companies'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('search/', CompanySearchView.as_view(), name='company-search'),
]