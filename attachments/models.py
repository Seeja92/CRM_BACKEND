from django.db import models

class Attachment(models.Model):
    ENTITY_TYPES = [
        ('deal',    'Deal'),
        ('company', 'Company'),
        ('lead',    'Lead'),
        ('ticket',  'Ticket'),
    ]

    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES)
    entity_id   = models.IntegerField()
    file        = models.FileField(upload_to='attachments/')
    file_name   = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.entity_type} - {self.file_name}"
