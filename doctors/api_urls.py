from rest_framework.routers import DefaultRouter
from .api_view import DoctorViewSet

router = DefaultRouter()
router.register(
    'Doctor',
    DoctorViewSet
)

urlpatterns = router.urls