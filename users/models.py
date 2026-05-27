from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Sales Manager', 'Sales Manager'),
        ('Sales Representative', 'Sales Representative'),
        ('Support Agent', 'Support Agent'),
        ('Marketing Manager', 'Marketing Manager'),
        ('Viewer', 'Viewer'),
    ]

    user             = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number     = models.CharField(max_length=20, blank=True)
    company_name     = models.CharField(max_length=200, blank=True)
    industry_type    = models.CharField(max_length=100, blank=True)
    country_or_region = models.CharField(max_length=100, blank=True)
    role             = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.role}"