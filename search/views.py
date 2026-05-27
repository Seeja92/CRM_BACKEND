from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from leads.models import Lead
from deals.models import Deal
from companies.models import Company
# from tickets.models import Ticket


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def global_search(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return Response({
            "leads": [],
            "deals": [],
            "companies": [],
            "tickets": [],
        })

    leads = Lead.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query)
    )[:5]

    deals = Deal.objects.filter(
        Q(deal_name__icontains=query)
    )[:5]

    companies = Company.objects.filter(
        Q(company_name__icontains=query) |
        Q(domain_name__icontains=query)
    )[:5]

    # tickets = Ticket.objects.filter(
    #     Q(title__icontains=query)
    # )[:5]

    return Response({
        "leads": [
            {
                "id": lead.id,
                "name": f"{lead.first_name} {lead.last_name}",
                "email": lead.email,
            }
            for lead in leads
        ],

        "deals": [
            {
                "id": deal.id,
                "name": deal.deal_name,
            }
            for deal in deals
        ],

        "companies": [
            {
                "id": company.id,
                "name": company.company_name,
            }
            for company in companies
        ],

    #     "tickets": [
    #         {
    #             "id": ticket.id,
    #             "name": ticket.title,
    #         }
    #         for ticket in tickets
    #     ],
    })