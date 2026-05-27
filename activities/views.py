from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Note, Call, Task, Meeting, Email
from .serializers import NoteSerializer, CallSerializer, TaskSerializer, MeetingSerializer, EmailSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone 
from twilio.rest import Client
from .services import initiate_twilio_call
from django.conf import settings

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class   = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        entity_type = self.request.query_params.get('entity_type')
        entity_id   = self.request.query_params.get('entity_id')
        qs = Note.objects.all()
        if entity_type:
            qs = qs.filter(entity_type=entity_type)
        if entity_id:
            qs = qs.filter(entity_id=entity_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CallViewSet(viewsets.ModelViewSet):
    serializer_class   = CallSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        entity_type = self.request.query_params.get('entity_type')
        entity_id   = self.request.query_params.get('entity_id')
        qs = Call.objects.all()
        if entity_type:
            qs = qs.filter(entity_type=entity_type)
        if entity_id:
            qs = qs.filter(entity_id=entity_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class TaskViewSet(viewsets.ModelViewSet):
    serializer_class   = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        entity_type = self.request.query_params.get('entity_type')
        entity_id   = self.request.query_params.get('entity_id')
        qs = Task.objects.all()
        if entity_type: qs = qs.filter(entity_type=entity_type)
        if entity_id:   qs = qs.filter(entity_id=entity_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MeetingViewSet(viewsets.ModelViewSet):
    serializer_class   = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        entity_type = self.request.query_params.get('entity_type')
        entity_id   = self.request.query_params.get('entity_id')
        qs = Meeting.objects.all()
        if entity_type: qs = qs.filter(entity_type=entity_type)
        if entity_id:   qs = qs.filter(entity_id=entity_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EmailViewSet(viewsets.ModelViewSet):
    serializer_class   = EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        entity_type = self.request.query_params.get('entity_type')
        entity_id   = self.request.query_params.get('entity_id')
        qs = Email.objects.all()
        if entity_type: qs = qs.filter(entity_type=entity_type)
        if entity_id:   qs = qs.filter(entity_id=entity_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_call(request):
    phone_number = request.data.get("to_phone")
    entity_type = request.data.get("entity_type")
    entity_id = request.data.get("entity_id")
    connected = request.data.get("connected", phone_number)

    if not phone_number:
        return Response({"error": "Phone number is required"}, status=400)

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        twilio_call = client.calls.create(
            to=phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            url="http://demo.twilio.com/docs/voice.xml"
        )

        now = timezone.now()

        Call.objects.create(
            entity_type=entity_type,
            entity_id=entity_id,
            connected=connected,
            phone_number=phone_number,
            call_outcome="Connected",
            twilio_sid=twilio_call.sid,
            call_status=twilio_call.status,
            date=now.date(),          
            time=now.strftime("%H:%M"),
            created_by=request.user,
        )
        return Response({"message": "Call initiated", "sid": twilio_call.sid})

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def end_call(request):
    sid = request.data.get("sid")

    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN
    )

    client.calls(sid).update(status="completed")

    return Response({
        "message": "Call ended"
    })