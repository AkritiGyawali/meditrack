from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import Record
from .serializers import RecordSerializer
from .permissions import IsAdminForDelete

class RecordViewSet(ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminForDelete]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['patient_name', 'contact', 'address', 'blood_group']
    ordering_fields = ['patient_name', 'age', 'id']
    ordering = ['patient_name']