import datetime
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth, TruncYear
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from deals.models import Deal
from leads.models import Lead

from .serializers import (
    DashboardStatsSerializer,
    ConversionStageSerializer,
    SalesDataPointSerializer,
    TeamMemberSerializer,
)

User = get_user_model()

def _lead_model():
    from leads.models import Lead
    return Lead

def _deal_model():
    from deals.models import Deal
    return Deal

def _company_model():
    from companies.models import Company
    return Company

# Explicitly mapping against the true strings found in your model choices
ACTIVE_STAGES_LOOKUP = [
    'Appointment Scheduled', 
    'Qualified to Buy', 
    'Presentation Scheduled', 
    'Decision Maker Bought In', 
    'Contract Sent', 
    'Proposal Sent', 
    'Negotiation'
]

MONTH_LABELS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# Maps your exact model database choices to dashboard presentation layers
CONVERSION_CONFIG = [
    ('Appointment Scheduled',   'Appointment Scheduled',   '#5b4fcf'),
    ('Qualified to Buy',       'Qualified to Buy',       '#06b6d4'),
    ('Presentation Scheduled',  'Presentation Scheduled',  '#eab308'),
    ('Decision Maker Bought In','Decision Maker Bought In','#6366f1'),
    ('Contract Sent',           'Contract Sent',           '#a855f7'),
    ('Proposal Sent',           'Proposal Sent',           '#f97316'),
    ('Negotiation',             'Negotiation',             '#3b82f6'),
    ('Closed Won',              'Closed Won',              '#10b981'),
    ('Closed Lost',             'Closed Lost',             '#ef4444'),
]


# ── 1. Stats ──────────────────────────────────────────────────────────────────
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Lead = _lead_model()
        Deal = _deal_model()
        Company = _company_model()

        today = datetime.date.today()
        month_start = today.replace(day=1)

        total_leads = Lead.objects.count()
        active_deals = Deal.objects.filter(deal_stage__in=ACTIVE_STAGES_LOOKUP).count()
        closed_deals = Deal.objects.filter(deal_stage='Closed Won').count()
        total_companies = Company.objects.count()
        
        monthly_revenue = (
            Deal.objects
            .filter(deal_stage='Closed Won', close_date__gte=month_start)
            .aggregate(total=Sum('amount'))['total'] or 0
        )

        data = {
            'total_leads': total_leads,
            'active_deals': active_deals,
            'closed_deals': closed_deals,
            'total_companies': total_companies,
            'monthly_revenue': float(monthly_revenue),
        }
        return Response(DashboardStatsSerializer(data).data)



class DashboardConversionView(APIView):
    def get(self, request):
        # 1. 📊 BASE DENOMINATOR: Count every single record in the LEADS table
        total_leads_base = Lead.objects.count()
        
        if total_leads_base == 0:
            return Response([])

        # 2. 🔍 LEADS PAGE QUERIES
        # Contact: Counts leads whose status is NOT 'New'
        contacted_leads_count = Lead.objects.exclude(status__iexact='New').count()

        # Qualified Lead: Counts leads explicitly marked as Qualified on the leads page
        # (Make sure 'Qualified' matches your exact lead status string!)
        qualified_leads_count = Lead.objects.filter(status__iexact='Qualified').count()

        # 3. 💼 DEALS PAGE QUERIES
        # Aggregates remaining downstream stages from your Deals model database table
        deal_counts = Deal.objects.aggregate(
            # Proposal Sent: Combines proposal and contract stages under Deals
            proposal_count=Count('id', filter=Q(deal_stage__in=['Proposal Sent', 'Contract Sent'])),
            
            # Negotiation: Exact match under Deals
            negotiation_count=Count('id', filter=Q(deal_stage='Negotiation')),
            
            # Closed Won: Exact match under Deals
            won_count=Count('id', filter=Q(deal_stage='Closed Won')),
            
            # Closed Lost: Exact match under Deals
            lost_count=Count('id', filter=Q(deal_stage='Closed Lost'))
        )

        # 4. 🧮 HELPER: Calculate exact percentages against the complete Leads base
        def calc_pct(stage_count):
            return round((stage_count / total_leads_base) * 100)

        # 5. 🗺️ MAPPING: Final clean tracking array matching your frontend layout labels
        funnel_data = [
            {
                "label": "Contact",
                "value": calc_pct(contacted_leads_count), # From Leads
                "color": "#5b4fcf"
            },
            {
                "label": "Qualified Lead",
                "value": calc_pct(qualified_leads_count), # From Leads
                "color": "#10b981"
            },
            {
                "label": "Proposal Sent",
                "value": calc_pct(deal_counts['proposal_count']), # From Deals 💼
                "color": "#f59e0b"
            },
            {
                "label": "Negotiation",
                "value": calc_pct(deal_counts['negotiation_count']), # From Deals 💼
                "color": "#6366f1"
            },
            {
                "label": "Closed Won",
                "value": calc_pct(deal_counts['won_count']), # From Deals
                "color": "#10b981"
            },
            {
                "label": "Closed Lost",
                "value": calc_pct(deal_counts['lost_count']), # From Deals
                "color": "#ef4444"
            }
        ]

        return Response(funnel_data) 
 
# # ── 3. Sales Chart ────────────────────────────────────────────────────────────
class DashboardSalesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Deal = _deal_model()
        period = request.query_params.get('period', 'monthly').lower()

        if period == 'yearly':
            rows = (
                Deal.objects
                .filter(deal_stage='Closed Won', close_date__isnull=False)
                .annotate(period_date=TruncYear('close_date'))
                .values('period_date')
                .annotate(value=Sum('amount'))
                .order_by('period_date')
            )
            data = [
                {'month': str(row['period_date'].year), 'value': float(row['value'] or 0)}
                for row in rows
            ]
        else:
            current_year = datetime.date.today().year
            rows = (
                Deal.objects
                .filter(deal_stage='Closed Won', close_date__year=current_year)
                .annotate(period_date=TruncMonth('close_date'))
                .values('period_date')
                .annotate(value=Sum('amount'))
                .order_by('period_date')
            )
            month_map = {row['period_date'].month: float(row['value'] or 0) for row in rows}
            data = [
                {'month': MONTH_LABELS[m - 1], 'value': month_map.get(m, 0)}
                for m in range(1, 13)
            ]

        return Response(SalesDataPointSerializer(data, many=True).data)


# ── 4. Team Performance ───────────────────────────────────────────────────────
class DashboardTeamPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Deal = _deal_model()
        today = datetime.date.today()
        this_month_start = today.replace(day=1)
        prev_month_end = this_month_start - datetime.timedelta(days=1)
        prev_month_start = prev_month_end.replace(day=1)

        users = User.objects.all()
        result = []

        for user in users:
            full_name = user.get_full_name()
            username = user.username

            # Query the Deal table matching the owner's name profile configurations manually
            user_deals = Deal.objects.filter(
                Q(deal_owner__iexact=full_name) | Q(deal_owner__iexact=username)
            ) if full_name else Deal.objects.filter(deal_owner__iexact=username)

            # Aggregate stats explicitly for this rep
            stats = user_deals.aggregate(
            active_count=Count('id', filter=Q(deal_stage__in=ACTIVE_STAGES_LOOKUP)),
            closed_count=Count('id', filter=Q(deal_stage='Closed Won')),
    
    # 🧠 CHANGE: Remove the close_date filter here to get LIFETIME revenue
            rev_lifetime=Sum('amount', filter=Q(deal_stage='Closed Won')), 
    
    # Keep these as-is for the percentage change calculations
            rev_this_month=Sum('amount', filter=Q(deal_stage='Closed Won', close_date__gte=this_month_start)),
            rev_prev_month=Sum('amount', filter=Q(deal_stage='Closed Won', close_date__gte=prev_month_start, close_date__lt=this_month_start))
)

# 🧠 CHANGE: Point this_rev to your new lifetime calculation
            lifetime_rev = float(stats['rev_lifetime'] or 0) 
            this_month_rev = float(stats['rev_this_month'] or 0)
            prev_month_rev = float(stats['rev_prev_month'] or 0)

            pct = ((this_month_rev - prev_month_rev) / prev_month_rev * 100) if prev_month_rev > 0 else 0.0
            positive = pct >= 0

            result.append({
                'id': user.id,
                'name': full_name or username,
                'active_deals': stats['active_count'] or 0,
                'closed_deals': stats['closed_count'] or 0,
                'revenue': f"${lifetime_rev:,.0f}",  # 👈 Displays everything now!
                'change': f"+{pct:.1f}%" if positive else f"{pct:.1f}%",
                'positive': positive,
                'raw_revenue': lifetime_rev  # Used for sorting table rows
})
            # stats = user_deals.aggregate(
            #     active_count=Count('id', filter=Q(deal_stage__in=ACTIVE_STAGES_LOOKUP)),
            #     closed_count=Count('id', filter=Q(deal_stage='Closed Won')),
            #     rev_this_month=Sum('amount', filter=Q(deal_stage='Closed Won', close_date__gte=this_month_start)),
            #     rev_prev_month=Sum('amount', filter=Q(deal_stage='Closed Won', close_date__gte=prev_month_start, close_date__lt=this_month_start))
            # )

            # this_rev = float(stats['rev_this_month'] or 0)
            # prev_rev = float(stats['rev_prev_month'] or 0)
            
            # pct = ((this_rev - prev_rev) / prev_rev * 100) if prev_rev > 0 else 0.0
            # positive = pct >= 0

            # result.append({
            #     'id': user.id,
            #     'name': full_name or username,
            #     'active_deals': stats['active_count'] or 0,
            #     'closed_deals': stats['closed_count'] or 0,
            #     'revenue': f"${this_rev:,.0f}",
            #     'change': f"+{pct:.1f}%" if positive else f"{pct:.1f}%",
            #     'positive': positive,
            #     'raw_revenue': this_rev  # Used purely for sorting below
            # })

        # Rank the performance table by top monthly revenue earners
        result.sort(key=lambda x: x['raw_revenue'], reverse=True)
        
        # Strip out raw temporary sort values before validating through DRF serializer
        for item in result:
            item.pop('raw_revenue', None)

        return Response(TeamMemberSerializer(result, many=True).data)