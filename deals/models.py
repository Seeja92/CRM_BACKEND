

from django.db import models
from django.contrib.auth.models import User

class Deal(models.Model):

    STAGE_CHOICES = [
        ('Appointment Scheduled', 'Appointment Scheduled'),
        ('Qualified to Buy', 'Qualified to Buy'),
        ('Presentation Scheduled', 'Presentation Scheduled'),
        ('Decision Maker Bought In', 'Decision Maker Bought In'),
        ('Contract Sent', 'Contract Sent'),
        ('Closed Won', 'Closed Won'),
        ('Closed Lost', 'Closed Lost'),
        ('Proposal Sent', 'Proposal Sent'),
        ('Negotiation', 'Negotiation'),
    ]

    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    deal_name       = models.CharField(max_length=255)
    deal_stage      = models.CharField(max_length=50, choices=STAGE_CHOICES)
    close_date      = models.DateField()
    # deal_owner      = models.CharField(max_length=255)
    deal_owner = models.ManyToManyField(
    User,
    related_name="owned_deals",
    blank=True
)
    amount          = models.DecimalField(max_digits=12, decimal_places=2)
    priority        = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    associated_lead = models.ForeignKey(
    'leads.Lead',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='deals',
    db_column='associated_lead_id'
)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.deal_name


class DealActivity(models.Model):
    deal            = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='activities')
    message         = models.TextField()
    activity_type   = models.CharField(max_length=50, default='stage_change')
    created_by_name = models.CharField(max_length=255, null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.activity_type} - {self.deal.deal_name}"