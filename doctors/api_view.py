from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import Doctor
from .serializers import DoctorSerializer
from .permissions import IsAdminForDelete

class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAdminForDelete]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['doctor_name', 'specialization', 'availability']
    ordering_fields = ['doctor_name', 'id']
    ordering = ['doctor_name']
    