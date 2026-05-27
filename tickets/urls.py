from django.urls import path
from .views import TicketListCreateView, TicketDetailView,import_tickets

urlpatterns = [
    path('',        TicketListCreateView.as_view(), name='ticket-list-create'),
    path('import/', import_tickets, name='import_tickets'),
    path('<int:pk>/', TicketDetailView.as_view(),   name='ticket-detail'),
]