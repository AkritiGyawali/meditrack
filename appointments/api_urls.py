from rest_framework.routers import DefaultRouter
from .api_view import AppointmentViewSet

router = DefaultRouter()
router.register(
    'Appointment',
    AppointmentViewSet
)
urlpatterns = router.urls