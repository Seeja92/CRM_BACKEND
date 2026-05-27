
import csv
import io
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Lead
from .serializers import LeadSerializer

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_date')
    serializer_class = LeadSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'company_name']

    def get_queryset(self):
        queryset = Lead.objects.all().order_by('-created_date')
        status = self.request.query_params.get('status')

        if status:
            queryset = queryset.filter(status=status)

        return queryset
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def import_leads(request):
    print("=" * 50)
    print("1. Import request received")
    print("2. User:", request.user)
    print("3. Files:", request.FILES)
    print("=" * 50)

    file = request.FILES.get('file')
    if not file:
        return Response({'detail': 'No file provided'}, status=400)

    try:
        decoded = file.read().decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(decoded))

        print("4. CSV columns:", reader.fieldnames)

        count = 0
        errors = []

        for i, row in enumerate(reader, start=1):
            print(f"Row {i}:", row)
            try:
                Lead.objects.create(
                    first_name=row.get('first_name', '').strip(),
                    last_name=row.get('last_name', '').strip(),
                    email=row.get('email', '').strip(),
                    phone=row.get('phone', '').strip(),
                    company_name=row.get('company_name', '').strip(),
                    job_title=row.get('job_title', '').strip(),
                    status=row.get('status', 'New').strip(),
                )
                count += 1
            except Exception as e:
                errors.append(f"Row {i}: {str(e)}")
                print(f"Row {i} error:", str(e))

        print("Imported count:", count)
        print("Errors:", errors)

        return Response({
            'imported_count': count,
            'errors': errors,
        })

    except Exception as e:
        print("Exception:", str(e))
        return Response({'detail': str(e)}, status=400)

