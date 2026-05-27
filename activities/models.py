from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    entity_type = models.CharField(max_length=20)  # lead, deal, company, ticket
    entity_id   = models.IntegerField()
    content     = models.TextField()
    created_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Call(models.Model):
    entity_type = models.CharField(max_length=20)
    entity_id = models.IntegerField()

    connected = models.CharField(max_length=255)

    # actual customer phone number
    phone_number = models.CharField(max_length=20)

    call_outcome = models.CharField(max_length=100)

    # Twilio call SID
    twilio_sid = models.CharField(max_length=255, blank=True)

    # call status
    call_status = models.CharField(
        max_length=50,
        default="initiated"
    )

    # duration in seconds
    duration = models.IntegerField(default=0)

    date = models.DateField()
    time = models.TimeField()

    note = models.TextField(blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Task(models.Model):
    PRIORITY_CHOICES = [('Low','Low'),('Medium','Medium'),('High','High'),('Urgent','Urgent')]
    TYPE_CHOICES     = [('To-Do','To-Do'),('Call','Call'),('Email','Email'),('Meeting','Meeting'),('Follow Up','Follow Up')]

    entity_type = models.CharField(max_length=20)
    entity_id   = models.IntegerField()
    task_name   = models.CharField(max_length=255)
    due_date    = models.DateField()
    time        = models.TimeField()
    task_type   = models.CharField(max_length=50, choices=TYPE_CHOICES)
    priority    = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    note        = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)
    created_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date', 'time']

class Meeting(models.Model):
    entity_type = models.CharField(max_length=20)
    entity_id   = models.IntegerField()
    title       = models.CharField(max_length=255)
    start_date  = models.DateField()
    start_time  = models.TimeField()
    end_time    = models.TimeField()
    attendees   = models.CharField(max_length=255, blank=True)
    location    = models.CharField(max_length=100, blank=True)
    reminder    = models.CharField(max_length=100, blank=True)
    note        = models.TextField(blank=True)
    created_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Email(models.Model):
    entity_type = models.CharField(max_length=20)
    entity_id   = models.IntegerField()
    recipients  = models.CharField(max_length=500)
    cc          = models.CharField(max_length=500, blank=True)
    bcc         = models.CharField(max_length=500, blank=True)
    subject     = models.CharField(max_length=255)
    body        = models.TextField(blank=True)
    created_by  = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_emails' 
    )
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']