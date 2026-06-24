from rest_framework.routers import DefaultRouter
from .api_view import AppointmentViewSet

router = DefaultRouter()
router.register(
    'appointment',
    AppointmentViewSet
)
urlpatterns = router.urls