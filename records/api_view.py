from rest_framework.viewsets import ModelViewSet
from .models import Record
from .serializers import RecordSerializer

class RecordViewSet(ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer