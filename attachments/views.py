from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Attachment
from .serializers import AttachmentSerializer


class AttachmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entity_type = request.query_params.get('entity_type')
        entity_id   = request.query_params.get('entity_id')

        if not entity_type or not entity_id:
            return Response(
                {'error': 'entity_type and entity_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        attachments = Attachment.objects.filter(
            entity_type=entity_type,
            entity_id=entity_id
        ).order_by('-uploaded_at')

        serializer = AttachmentSerializer(attachments, many=True)
        return Response(serializer.data)

    def post(self, request):
        file      = request.FILES.get('file')
        entity_type = request.data.get('entity_type')
        entity_id   = request.data.get('entity_id')

        if not file or not entity_type or not entity_id:
            return Response(
                {'error': 'file, entity_type and entity_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        attachment = Attachment.objects.create(
            entity_type = entity_type,
            entity_id   = int(entity_id),
            file        = file,
            file_name   = file.name,
        )

        serializer = AttachmentSerializer(attachment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AttachmentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            attachment = Attachment.objects.get(pk=pk)
            attachment.file.delete()
            attachment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Attachment.DoesNotExist:
            return Response(
                {'error': 'Attachment not found'},
                status=status.HTTP_404_NOT_FOUND
            )