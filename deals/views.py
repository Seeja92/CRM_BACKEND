
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
import csv
import io
from .models import Deal, DealActivity
from .serializers import DealSerializer, DealActivitySerializer


# class DealListCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # deals      = Deal.objects.all().order_by('-created_at')
#         user = request.user
#         role = user.profile.role

#         if role == "Admin":
#             deals = Deal.objects.all().order_by("-created_at")
#         else:
#             deals = Deal.objects.filter(
#             deal_owner=user.get_full_name()
#             ).order_by("-created_at")
#         serializer = DealSerializer(deals, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = DealSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DealListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = user.profile.role

        if role == "Admin":
            deals = Deal.objects.all().order_by("-created_at")
        else:
            deals = Deal.objects.filter(
                deal_owner=user
            ).distinct().order_by("-created_at")

        serializer = DealSerializer(deals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DealSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class DealDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Deal.objects.get(pk=pk)
        except Deal.DoesNotExist:
            return None

    def get(self, request, pk):
        deal = self.get_object(pk)
        if not deal:
            return Response({'error': 'Deal not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        role = user.profile.role

        if (
            role != "Admin"
            and deal.deal_owner != user.get_full_name()
        ):
            return Response(
                {"detail": "Permission denied"},
                status=403
        )
        return Response(DealSerializer(deal).data)
        

    # def put(self, request, pk):
    #    deal = self.get_object(pk)
    #     if not deal:
    #         return Response({'error': 'Deal not found'}, status=status.HTTP_404_NOT_FOUND)
    #         serializer = DealSerializer(deal, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data) 
    #    user = request.user
    #    role = user.profile.role

    #    if (
    #     role != "Admin"
    #     and deal.deal_owner != user.get_full_name()
    #    ):
    #         return Response(
    #             {"detail": "You can edit only your deals."},
    #             status=403
    #         ) 


        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        deal = self.get_object(pk)

        if not deal:
            return Response(
                {'error': 'Deal not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user
        role = user.profile.role

        if (
            role != "Admin"
            and deal.deal_owner != user.get_full_name()
        ):
            return Response(
                {"detail": "You can edit only your deals."},
                status=403
            )

        serializer = DealSerializer(
            deal,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # def delete(self, request, pk):
    #     deal = self.get_object(pk)
    #     if not deal:
    #         return Response({'error': 'Deal not found'}, status=status.HTTP_404_NOT_FOUND)
    #     deal.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    def delete(self, request, pk):
        deal = self.get_object(pk)

        if not deal:
            return Response(
                {'error': 'Deal not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user
        role = user.profile.role

        if role != "Admin":
            return Response(
                {"detail": "Only Admin can delete deals."},
                status=403
            )

        deal.delete()

        return Response(
            {"message": "Deal deleted successfully."},
            status=204
        )

class DealActivityListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, deal_id):
        activities = DealActivity.objects.filter(deal_id=deal_id)
        serializer = DealActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request, deal_id):
        try:
            deal = Deal.objects.get(pk=deal_id)
        except Deal.DoesNotExist:
            return Response({'error': 'Deal not found'}, status=status.HTTP_404_NOT_FOUND)

        # ── Get current user name ──
        user       = request.user
        user_name  = user.get_full_name() or user.username or user.email or ''

        serializer = DealActivitySerializer(data={
            'deal':            deal.id,
            'message':         request.data.get('message', ''),
            'activity_type':   request.data.get('activity_type', 'stage_change'),
            'created_by_name': user_name,
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def import_deals(request):
    print("=" * 50)
    print("1. Deal import request received")
    print("2. User:", request.user)
    print("3. Files:", request.FILES)
    print("=" * 50)

    file = request.FILES.get('file')
    if not file:
        return Response({'detail': 'No file provided'}, status=400)

    try:
        decoded = file.read().decode('utf-8-sig')
        reader  = csv.DictReader(io.StringIO(decoded))
        print("4. CSV columns:", reader.fieldnames)

        count  = 0
        errors = []

        for i, row in enumerate(reader, start=1):
            print(f"Row {i}:", row)
            try:
                Deal.objects.create(
                    deal_name       = row.get('deal_name',  '').strip(),
                    deal_stage      = row.get('deal_stage', '').strip(),
                    amount          = row.get('amount', 0),
                    deal_owner      = row.get('deal_owner', '').strip(),
                    close_date      = row.get('close_date', '').strip(),
                    priority        = row.get('priority', 'Medium').strip(),
                    associated_lead = row.get('associated_lead', '').strip() or None,
                )
                count += 1
            except Exception as e:
                errors.append(f"Row {i}: {str(e)}")
                print(f"Row {i} error:", str(e))

        print("Imported count:", count)
        print("Errors:", errors)

        return Response({'imported_count': count, 'errors': errors})

    except Exception as e:
        print("Exception:", str(e))
        return Response({'detail': str(e)}, status=400)