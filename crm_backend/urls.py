
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/auth/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/v1/leads/', include('leads.urls')),
    path('api/v1/deals/', include('deals.urls')),
    path('api/v1/companies/', include('companies.urls')),
    path('api/v1/tickets/', include('tickets.urls')),
    path('api/v1/activities/', include('activities.urls')),
    path('api/v1/attachments/', include('attachments.urls')),
    path('api/v1/search/', include('search.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/dashboard/', include('dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)