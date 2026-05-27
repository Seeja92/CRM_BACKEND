from django.urls import path
from .views import AttachmentListCreateView, AttachmentDeleteView

urlpatterns = [
    path('',        AttachmentListCreateView.as_view(), name='attachment-list-create'),
    path('<int:pk>/', AttachmentDeleteView.as_view(),   name='attachment-delete'),
]