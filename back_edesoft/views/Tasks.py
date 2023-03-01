from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.tools.auth import SecretsTokenAuthentication
from core.tasks import csv_to_db
from back_edesoft.serializers import TaskSerializer

@extend_schema(tags=["Tasks"])
class TasksViewSet(viewsets.GenericViewSet):
    authentication_classes = [SecretsTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    @action(detail=False, methods=['post'])
    def ImportCsv(self, request):
        bucket_name = request.data.get('bucket_name')
        object_key = request.data.get('object_key')
        if not bucket_name or not object_key:
            return Response({'error': 'Missing bucket_name or object_key'}, status=status.HTTP_400_BAD_REQUEST)
        task = csv_to_db.delay(bucket_name, object_key)
        return Response({'task_status': task.status}, status=status.HTTP_200_OK)

