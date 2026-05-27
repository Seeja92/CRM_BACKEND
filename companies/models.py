from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    INDUSTRY_CHOICES = [
        ('Legal Services', 'Legal Services'),
        ('Healthcare', 'Healthcare'),
        ('Real Estate', 'Real Estate'),
        ('Financial Advisory', 'Financial Advisory'),
        ('Retail & E-commerce', 'Retail & E-commerce'),
        ('Logistics & Supply Chain', 'Logistics & Supply Chain'),
        ('Marketing Agencies', 'Marketing Agencies'),
        ('Education Technology', 'Education Technology'),
        ('Technology', 'Technology'),
        ('Finance', 'Finance'),
        ('Manufacturing', 'Manufacturing'),
        ('Other', 'Other'),
    ]

    TYPE_CHOICES = [
        ('Prospect', 'Prospect'),
        ('Customer', 'Customer'),
        ('Partner', 'Partner'),
        ('Vendor', 'Vendor'),
        ('Other', 'Other'),
    ]

    domain_name    = models.CharField(max_length=255)
    company_name   = models.CharField(max_length=255)
    company_owner  = models.ManyToManyField(User, related_name='owned_companies', blank=True)
    industry       = models.CharField(max_length=100, choices=INDUSTRY_CHOICES)
    type           = models.CharField(max_length=50, choices=TYPE_CHOICES)
    city           = models.CharField(max_length=100, blank=True, null=True)
    country        = models.CharField(max_length=100, blank=True, null=True)
    no_of_employees = models.CharField(max_length=50, blank=True, null=True)
    annual_revenue = models.CharField(max_length=100, blank=True, null=True)
    email          = models.EmailField(blank=True, null=True)
    phone_number   = models.CharField(max_length=20)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company_name