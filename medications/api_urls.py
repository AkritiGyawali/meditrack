from rest_framework.routers import DefaultRouter
from .api_view import MedicationViewSet

router = DefaultRouter()

router.register(
    'medication',
    MedicationViewSet
)

urlpatterns = router.urls