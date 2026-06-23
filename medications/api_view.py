from rest_framework.viewsets import ModelViewSet
from .models import Medication
from .serializers import MedicationSerializer


class MedicationViewSet(ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class= MedicationSerializer
    