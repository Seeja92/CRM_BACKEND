from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Open','Open'),
        ('Waiting on us', 'Waiting on us'),
        ('Waiting on customer', 'Waiting on customer'),
        ('Resolved','Resolved'),
        ('Closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    SOURCE_CHOICES = [
        ('Chat', 'Chat'),
        ('Email', 'Email'),
        ('Phone', 'Phone'),
        ('Meeting','Meeting'),
    ]

    ticket_name    = models.CharField(max_length=255)
    company        = models.ForeignKey('companies.Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    deal           = models.ForeignKey('deals.Deal', on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    status         = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
    source         = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='Chat')
    priority       = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    ticket_owner   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.ticket_name