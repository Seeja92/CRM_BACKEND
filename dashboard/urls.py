

from django.urls import path
from .views import (
    DashboardStatsView,
    DashboardConversionView,
    DashboardSalesView,
    DashboardTeamPerformanceView,
)

urlpatterns = [
    path('stats/',            DashboardStatsView.as_view(),           name='dashboard-stats'),
    path('conversion/',       DashboardConversionView.as_view(),      name='dashboard-conversion'),
    path('sales/',            DashboardSalesView.as_view(),           name='dashboard-sales'),
    path('team-performance/', DashboardTeamPerformanceView.as_view(), name='dashboard-team'),
]