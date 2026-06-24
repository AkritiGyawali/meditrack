from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import IsAdminForDelete

class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAdminForDelete]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['patient_name__patient_name', 'doctor_name__doctor_name', 'status']
    ordering_fields = ['date', 'time', 'status', 'id']
    ordering = ['-date', '-time']
    