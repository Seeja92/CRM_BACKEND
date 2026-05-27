from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("lead", "Lead"),
        ("deal", "Deal"),
        ("ticket", "Ticket"),
        ("company", "Company"),
        ("reminder", "Reminder"),
        ("delete", "Deleted Resource"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPES,
        default="system"
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    related_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title