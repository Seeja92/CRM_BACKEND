from django.urls import path
from .views import notification_list,  mark_notifications_read, clear_notifications

urlpatterns = [
    path("", notification_list),
    path("mark-read/", mark_notifications_read),
    path("clear/", clear_notifications),
]