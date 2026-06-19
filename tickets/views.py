# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from django.db.models import Q
# from .models import Ticket
# from .serializers import TicketSerializer
# import csv
# import io

# from rest_framework.decorators import api_view, permission_classes
# from leads.models import Lead


# class TicketListCreateView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         tickets = Ticket.objects.select_related(
#         'deal__associated_lead',
#         'ticket_owner',
#         'company'
#     ).all()

#     def get(self, request):
#         tickets = Ticket.objects.all()

#         city = request.query_params.get('city')
#         if city:
#              tickets = tickets.filter(
#         Q(deal__associated_lead__city__icontains=city) |
#         Q(lead__city__icontains=city) |
#         Q(company__city__icontains=city)
#     )
#         search = request.query_params.get('search', '')
#         if search:
#             tickets = tickets.filter(
#                 Q(ticket_name__icontains=search) |
#                 Q(ticket_owner__first_name__icontains=search) |
#                 Q(ticket_owner__last_name__icontains=search) |
#                 Q(company__company_name__icontains=search) |
#                 Q(company__city__icontains=search) |
#                 Q(deal__deal_name__icontains=search) |
#                 Q(deal__associated_lead__city__icontains=search)
#             )

#         status_filter = request.query_params.get('status')
#         if status_filter:
#          tickets = tickets.filter(status=status_filter)

#         priority = request.query_params.get('priority')
#         if priority:
#          tickets = tickets.filter(priority=priority)

#         source = request.query_params.get('source')
#         if source:
#          tickets = tickets.filter(source=source)

#         owner = request.query_params.get('owner')
#         if owner:
#          tickets = tickets.filter(ticket_owner__id=owner)       

#         serializer = TicketSerializer(tickets, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = TicketSerializer(
#             data=request.data,
#             context={"request": request}
#         )

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TicketDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):
#         try:
#             return Ticket.objects.get(pk=pk)
#         except Ticket.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         ticket = self.get_object(pk)
#         if not ticket:
#             return Response({'error': 'Ticket not found'}, status=404)

#         serializer = TicketSerializer(ticket)
#         return Response(serializer.data)
#     def put(self, request, pk):
#         ticket = self.get_object(pk)
#         if not ticket:
#             return Response({'error': 'Ticket not found'}, status=404)
#         serializer = TicketSerializer(ticket, data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         ticket = self.get_object(pk)
#         if not ticket:
#             return Response({'error': 'Ticket not found'}, status=404)
#         ticket.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def import_tickets(request):

#     file = request.FILES.get('file')

#     if not file:
#         return Response({'detail': 'No file provided'}, status=400)

#     try:
#         decoded = file.read().decode('utf-8-sig')
#         reader = csv.DictReader(io.StringIO(decoded))

#         count = 0
#         errors = []

#         for i, row in enumerate(reader, start=1):
#             try:
#                 lead_email = row.get('email')
#                 city = row.get('city')

#                 lead = None

#                 if lead_email:
#                     lead = Lead.objects.filter(email=lead_email).first()

#                 if not lead and lead_email:
#                     lead = Lead.objects.create(
#                         email=lead_email,
#                         city=city
#                     )

#                 Ticket.objects.create(
#                     ticket_name=row.get('ticket_name', '').strip(),
#                     status=row.get('status', 'New').strip(),
#                     priority=row.get('priority', 'Medium').strip(),
#                     source=row.get('source', 'Chat').strip(),
#                     ticket_owner=request.user,
#                     lead=lead
#                 )

#                 count += 1

#             except Exception as e:
#                 errors.append(f"Row {i}: {str(e)}")

#         return Response({
#             'imported_count': count,
#             'errors': errors,
#         })

#     except Exception as e:
#         return Response({'detail': str(e)}, status=400)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Ticket
from .serializers import TicketSerializer
import csv
import io

from rest_framework.decorators import api_view, permission_classes
from leads.models import Lead


class TicketListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.select_related(
            'deal__associated_lead',
            'ticket_owner',
            'company'
        ).all()

        city = request.query_params.get('city')
        if city:
            tickets = tickets.filter(
                Q(deal__associated_lead__city__icontains=city) |
                Q(lead__city__icontains=city) |
                Q(company__city__icontains=city)
            )

        search = request.query_params.get('search', '')
        if search:
            tickets = tickets.filter(
                Q(ticket_name__icontains=search) |
                Q(ticket_owner__first_name__icontains=search) |
                Q(ticket_owner__last_name__icontains=search) |
                Q(company__company_name__icontains=search) |
                Q(company__city__icontains=search) |
                Q(deal__deal_name__icontains=search) |
                Q(deal__associated_lead__city__icontains=search)
            )

        status_filter = request.query_params.get('status')
        if status_filter:
            tickets = tickets.filter(status=status_filter)

        priority = request.query_params.get('priority')
        if priority:
            tickets = tickets.filter(priority=priority)

        source = request.query_params.get('source')
        if source:
            tickets = tickets.filter(source=source)

        owner = request.query_params.get('owner')
        if owner:
            tickets = tickets.filter(ticket_owner__id=owner)

        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TicketSerializer(
            data=request.data,
            context={"request": request}
        )
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
            return Response({'error': 'Ticket not found'}, status=404)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, pk):
        ticket = self.get_object(pk)
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=404)
        serializer = TicketSerializer(ticket, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ticket = self.get_object(pk)
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=404)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
                lead_email = row.get('email')
                city = row.get('city')
                lead = None

                if lead_email:
                    lead = Lead.objects.filter(email=lead_email).first()

                if not lead and lead_email:
                    lead = Lead.objects.create(
                        email=lead_email,
                        city=city
                    )

                Ticket.objects.create(
                    ticket_name=row.get('ticket_name', '').strip(),
                    status=row.get('status', 'New').strip(),
                    priority=row.get('priority', 'Medium').strip(),
                    source=row.get('source', 'Chat').strip(),
                    ticket_owner=request.user,
                    lead=lead
                )
                count += 1

            except Exception as e:
                errors.append(f"Row {i}: {str(e)}")

        return Response({'imported_count': count, 'errors': errors})

    except Exception as e:
        return Response({'detail': str(e)}, status=400)