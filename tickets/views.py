from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Ticket
from .serializers import TicketSerializer
from rest_framework.decorators import api_view, permission_classes

    
import csv
import io

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class TicketListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.all()

        # ── Filters ───────────────────────────────────────────────────────────
        search = request.query_params.get('search', '')
        if search:
            tickets = tickets.filter(
                Q(ticket_name__icontains=search) |
                Q(ticket_owner__first_name__icontains=search) |
                Q(ticket_owner__last_name__icontains=search) |
                Q(company__company_name__icontains=search) |
                Q(deal__deal_name__icontains=search)
            )

        status_filter = request.query_params.get('status', '')
        if status_filter:
            tickets = tickets.filter(status=status_filter)

        priority_filter = request.query_params.get('priority', '')
        if priority_filter:
            tickets = tickets.filter(priority=priority_filter)

        source_filter = request.query_params.get('source', '')
        if source_filter:
            tickets = tickets.filter(source=source_filter)

        owner_filter = request.query_params.get('owner', '')
        if owner_filter:
           tickets = tickets.filter(ticket_owner__id=owner_filter)


        company_filter = request.query_params.get('company_id', '')
        if company_filter:
            tickets = tickets.filter(company__id=company_filter)

        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
    
    

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return None

    def get(self, request, pk):
        ticket = self.get_object(pk)
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, pk):
        ticket = self.get_object(pk)
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ticket = self.get_object(pk)
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from .models import Ticket


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_tickets(request):

    file = request.FILES.get('file')

    if not file:
        return Response({'detail': 'No file provided'}, status=400)

    try:
        decoded = file.read().decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(decoded))

        count = 0
        errors = []

        for i, row in enumerate(reader, start=1):
            try:
                Ticket.objects.create(
                    ticket_name=row.get('ticket_name', '').strip(),
                    status=row.get('status', 'New').strip(),
                    priority=row.get('priority', 'Medium').strip(),
                    source=row.get('source', 'Chat').strip(),
                    ticket_owner=request.user,  
                )

                count += 1

            except Exception as e:
                errors.append(f"Row {i}: {str(e)}")

        return Response({
            'imported_count': count,
            'errors': errors,
        })

    except Exception as e:
        return Response({'detail': str(e)}, status=400)