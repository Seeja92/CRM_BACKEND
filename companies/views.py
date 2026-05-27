from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Company
from .serializers import CompanySerializer, CompanyListSerializer
import csv
import io
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class CompanyListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Search
        search = request.query_params.get('search', '')
        industry = request.query_params.get('industry', '')
        city = request.query_params.get('city', '')
        country = request.query_params.get('country', '')

        companies = Company.objects.all()

        if search:
            companies = companies.filter(
                company_name__icontains=search
            ) | companies.filter(
                phone_number__icontains=search
            ) | companies.filter(
                city__icontains=search
            ) | companies.filter(
                company_owner__first_name__icontains=search
            ) | companies.filter(
                company_owner__last_name__icontains=search
            )

        if industry:
            companies = companies.filter(industry=industry)

        if city:
            companies = companies.filter(city__icontains=city)

        if country:
            companies = companies.filter(country__icontains=country)

        companies = companies.distinct()
        serializer = CompanyListSerializer(companies, many=True)
        return Response({
            'count': companies.count(),
            'results': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
     serializer = CompanySerializer(data=request.data)

     if serializer.is_valid():
        company = serializer.save()

        # Assign logged-in user automatically
        company.company_owner.add(request.user)

        return Response({
            'message': 'Company created successfully.',
            'data': CompanySerializer(company).data,
        }, status=status.HTTP_201_CREATED)

     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Company updated successfully.',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Company updated successfully.',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        company.delete()
        return Response({
            'message': 'Company deleted successfully.',
        }, status=status.HTTP_204_NO_CONTENT)


class CompanySearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.query_params.get('q', '')
        if not search:
            return Response([], status=status.HTTP_200_OK)

        companies = Company.objects.filter(
            company_name__icontains=search
        ).values('id', 'company_name')[:10]

        return Response(list(companies), status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def import_companies(request):

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
                company =Company.objects.create(
                    domain_name=row.get('domain_name', '').strip(),
                    company_name=row.get('company_name', '').strip(),
                    industry=row.get('industry', '').strip(),
                    type=row.get('type', '').strip(),
                    city=row.get('city', '').strip(),
                    country=row.get('country', '').strip(),
                    no_of_employees=row.get('no_of_employees', '').strip(),
                    annual_revenue=row.get('annual_revenue', '').strip(),
                    email=row.get('email', '').strip(),
                    phone_number=row.get('phone_number', '').strip(),
                )
                company.company_owner.add(request.user)
                count += 1

            except Exception as e:
                errors.append(f"Row {i}: {str(e)}")

        return Response({
            'imported_count': count,
            'errors': errors,
        })

    except Exception as e:
        return Response({'detail': str(e)}, status=400)