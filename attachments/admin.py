from django.contrib import admin
from .models import Attachment

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'entity_type', 'entity_id', 'file_name', 'uploaded_at']
    list_filter  = ['entity_type']