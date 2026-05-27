from rest_framework import serializers
from .models import Note, Call,Task,Meeting,Email

class NoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model  = Note
        fields = ['id', 'entity_type', 'entity_id', 'content',
                  'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
        return "Unknown"

class CallSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model  = Call
        fields = ['id', 'entity_type', 'entity_id', 'connected', 'call_outcome',
                  'date', 'time', 'note', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
        return "Unknown"
class TaskSerializer(serializers.ModelSerializer):
    created_by_name  = serializers.SerializerMethodField()
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model  = Task
        fields = ['id', 'entity_type', 'entity_id', 'task_name', 'due_date',
                  'time', 'task_type', 'priority', 'assigned_to', 'assigned_to_name',
                  'note', 'is_complete', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
        return "Unknown"

    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return f"{obj.assigned_to.first_name} {obj.assigned_to.last_name}".strip() or obj.assigned_to.username
        return "Unknown"

class MeetingSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model  = Meeting
        fields = ['id', 'entity_type', 'entity_id', 'title', 'start_date',
                  'start_time', 'end_time', 'attendees', 'location', 'reminder',
                  'note', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
        return "Unknown"

class EmailSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model  = Email
        fields = ['id', 'entity_type', 'entity_id', 'recipients', 'cc', 'bcc',
                  'subject', 'body', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
        return "Unknown"