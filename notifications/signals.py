from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# ── Import Your Core Target Models ──────────────────────────────────────────

from leads.models import Lead
from deals.models import Deal
from companies.models import Company
from tickets.models import Ticket
from .models import Notification

User = get_user_model()

# Helper function to distribute notifications to all active CRM users
def broadcast_notification(title, message, notification_type, related_id=None):
    users = User.objects.filter(is_active=True)
    notifications_to_create = [
        Notification(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            related_id=related_id
        )
        for user in users
    ]
    Notification.objects.bulk_create(notifications_to_create)

# ── 1. GLOBAL LEADS LISTENER ──────────────────────────────────────────────────
@receiver(post_save, sender=Lead)
def lead_save_handler(sender, instance, created, **kwargs):
    if created:
        broadcast_notification(
            title="New Lead Created 🟢",
            message=f"Lead '{instance.first_name} {instance.last_name}' was added to the CRM.",
            notification_type="lead",
            related_id=instance.id
        )
    else:
        broadcast_notification(
            title="Lead Updated 🔵",
            message=f"Information for lead '{instance.first_name} {instance.last_name}' has been modified.",
            notification_type="lead",
            related_id=instance.id
        )

@receiver(post_delete, sender=Lead)
def lead_delete_handler(sender, instance, **kwargs):
    broadcast_notification(
        title="Lead Removed 🔴",
       message=f"Lead '{instance.first_name} {instance.last_name}' was permanently deleted.",
        notification_type="delete",
        related_id=None # None prevents broken links on the frontend
    )

# ── 2. GLOBAL DEALS LISTENER ──────────────────────────────────────────────────
@receiver(post_save, sender=Deal)
def deal_save_handler(sender, instance, created, **kwargs):
    if created:
        broadcast_notification(
            title="New Opportunity Logged 🟢",
            message=f"Deal '{instance.deal_name}' was introduced to the pipeline.",
            notification_type="deal",
            related_id=instance.id
        )
    else:
        broadcast_notification(
            title="Deal Pipeline Progressed 🔵",
            message=f"Deal '{instance.deal_name}' progress attributes were modified.",
            notification_type="deal",
            related_id=instance.id
        )

@receiver(post_delete, sender=Deal)
def deal_delete_handler(sender, instance, **kwargs):
    broadcast_notification(
        title="Deal Pipeline Purged 🔴",
        message=f"Deal '{instance.deal_name}' was deleted from active pipelines.",
        notification_type="delete",
        related_id=None
    )

# ── 3. GLOBAL COMPANIES LISTENER ──────────────────────────────────────────────
@receiver(post_save, sender=Company)
def company_save_handler(sender, instance, created, **kwargs):
    if created:
        broadcast_notification(
            title="New Company Profile 🟢",
            message=f"Company account '{instance.company_name}' has been registered.",
            notification_type="company",
            related_id=instance.id
        )
    else:
        broadcast_notification(
            title="Company Profile Modified 🔵",
            message=f"Profile data for '{instance.company_name}' was updated.",
            notification_type="company",
            related_id=instance.id
        )

@receiver(post_delete, sender=Company)
def company_delete_handler(sender, instance, **kwargs):
    broadcast_notification(
        title="Company Profile Deleted 🔴",
        message=f"Account directory '{instance.company_name}' was removed from the CRM.",
        notification_type="delete",
        related_id=None
    )


    # ── 4. GLOBAL TICKETS LISTENER ────────────────────────────────────────────────
@receiver(post_save, sender=Ticket)
def ticket_save_handler(sender, instance, created, **kwargs):
    if created:
        broadcast_notification(
            title="New Support Ticket 🟢",
            message=f"Ticket #{instance.id} '{instance.ticket_name}' has been opened.",
            notification_type="ticket",
            related_id=instance.id
        )
    else:
        broadcast_notification(
            title="Ticket Status Updated 🔵",
            message=f"Ticket #{instance.id} details or status were updated.",
            notification_type="ticket",
            related_id=instance.id
        )

@receiver(post_delete, sender=Ticket)
def ticket_delete_handler(sender, instance, **kwargs):
    broadcast_notification(
        title="Ticket Permanently Closed/Deleted 🔴",
        message=f"Ticket #{instance.id} was removed from the database.",
        notification_type="delete",
        related_id=None
    )