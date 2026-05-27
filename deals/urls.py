from django.urls import path
from .views import DealListCreateView, DealDetailView, DealActivityListCreateView,import_deals

urlpatterns = [
    path('',                            DealListCreateView.as_view(),         name='deal-list-create'),         
    path('import/', import_deals, name='import_deals'),
    path('<int:pk>/',                   DealDetailView.as_view(),              name='deal-detail'),
    path('<int:deal_id>/activities/',   DealActivityListCreateView.as_view(),  name='deal-activities'),
]