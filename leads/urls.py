

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, import_leads

router = DefaultRouter()
router.register(r'', LeadViewSet, basename='lead')

urlpatterns = [
    path('import/', import_leads, name='leads-import'), 
    path('', include(router.urls)),
]