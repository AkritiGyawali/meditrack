from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import Medication
from .serializers import MedicationSerializer
from  .permissions import IsAdminForDelete

class MedicationViewSet(ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class= MedicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminForDelete]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['patient_name__patient_name', 'medication_name', 'dosage', 'frequency']
    ordering_fields = ['medication_name', 'start_date', 'end_date', 'id']
    ordering = ['-start_date', 'medication_name']
    