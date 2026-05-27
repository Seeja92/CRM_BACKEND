from rest_framework import serializers
from .models import Attachment

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Attachment
        fields = ['id', 'entity_type', 'entity_id', 'file', 'file_name', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']