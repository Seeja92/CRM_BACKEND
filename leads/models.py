from django.db import models
from django.contrib.auth.models import User
from companies.models import Company

class Lead(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Qualified', 'Qualified'),
        ('Converted', 'Converted'),
        ('Unqualified', 'Unqualified'),
        ('Attempted to Contact', 'Attempted to Contact'),
        ('Contacted', 'Contacted'),
        ('Closed', 'Closed'),
    ]

    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    email         = models.EmailField(unique=True)
    phone         = models.CharField(max_length=20)
    company       = models.ForeignKey(          # ← add this
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads'
    )
    company_name  = models.CharField(max_length=200, blank=True, null=True)
    job_title     = models.CharField(max_length=100, blank=True, null=True)
    # contact_owner = models.CharField(max_length=200, blank=True, null=True)
    contact_owner = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="owned_leads"
)
#     contact_owner = models.ForeignKey(
#     User,
#     on_delete=models.SET_NULL,
#     null=True,
#     blank=True,
#     related_name="owned_leads"
# )
    status        = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
    city = models.CharField(
    max_length=100,
    blank=True,
    null=True
)
    created_date  = models.DateTimeField(auto_now_add=True)
    updated_date  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"