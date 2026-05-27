from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Deal
from notifications.models import Notification
from django.contrib.auth import get_user_model
from datetime import date

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


# Store old stage before save
@receiver(pre_save, sender=Deal)
def store_old_deal_stage(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Deal.objects.get(pk=instance.pk)
            instance._old_stage = old.deal_stage
        except Deal.DoesNotExist:
            instance._old_stage = None
    else:
        instance._old_stage = None


@receiver(post_save, sender=Deal)
def deal_notification(sender, instance, created, **kwargs):
    if created:
        notify_all(
            title="New Deal Added",
            message=f"{instance.deal_name} worth ${instance.amount} was added",
            notification_type="deal",
            related_id=instance.id
        )
    else:
        old_stage = getattr(instance, '_old_stage', None)

        if old_stage and old_stage != instance.deal_stage:
            # Stage changed
            notify_all(
                title="Deal Stage Updated",
                message=f"{instance.deal_name} moved from {old_stage} to {instance.deal_stage}",
                notification_type="deal",
                related_id=instance.id
            )
            # Closed won special notification
            if instance.deal_stage == "Closed Won":
                notify_all(
                    title="Deal Closed — Won! 🎉",
                    message=f"{instance.deal_name} worth ${instance.amount} was closed successfully",
                    notification_type="deal",
                    related_id=instance.id
                )
        else:
            # General update
            notify_all(
                title="Deal Updated",
                message=f"{instance.deal_name} details were updated",
                notification_type="deal",
                related_id=instance.id
            )

        # Closing date passed
        if (instance.close_date and
            instance.close_date < date.today() and
            instance.deal_stage not in ["Closed Won", "Closed Lost"]):
            notify_all(
                title="Deal Closing Date Passed",
                message=f"{instance.deal_name} closing date has passed — still in {instance.deal_stage}",
                notification_type="deal",
                related_id=instance.id
            )


@receiver(post_delete, sender=Deal)
def deal_deleted_notification(sender, instance, **kwargs):
    notify_all(
        title="Deal Deleted",
        message=f"{instance.deal_name} worth ${instance.amount} was deleted",
        notification_type="deal",
        related_id=None
    )