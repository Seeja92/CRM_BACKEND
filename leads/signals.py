from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Lead
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()


def notify_all(title, message, notification_type, related_id):
    users = User.objects.filter(is_active=True)
    Notification.objects.bulk_create([
        Notification(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            related_id=related_id
        ) for user in users
    ])


# Store old values before save
@receiver(pre_save, sender=Lead)
def store_old_lead_values(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Lead.objects.get(pk=instance.pk)
            instance._old_status = old.status
        except Lead.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Lead)
def lead_notification(sender, instance, created, **kwargs):
    name = f"{instance.first_name} {instance.last_name}"
    company = instance.company_name or "Unknown Company"

    if created:
        notify_all(
            title="New Lead Added",
            message=f"{name} from {company} was added",
            notification_type="lead",
            related_id=instance.id
        )
    else:
        old_status = getattr(instance, '_old_status', None)
        if old_status and old_status != instance.status:
            notify_all(
                title="Lead Status Updated",
                message=f"{name} status changed from {old_status} to {instance.status}",
                notification_type="lead",
                related_id=instance.id
            )
        else:
            notify_all(
                title="Lead Updated",
                message=f"{name} details were updated",
                notification_type="lead",
                related_id=instance.id
            )


@receiver(post_delete, sender=Lead)
def lead_deleted_notification(sender, instance, **kwargs):
    name = f"{instance.first_name} {instance.last_name}"
    notify_all(
        title="Lead Deleted",
        message=f"{name} from {instance.company_name or 'Unknown Company'} was deleted",
        notification_type="lead",
        related_id=None
    )