from rest_framework.routers import DefaultRouter
from .api_view import RecordViewSet

router = DefaultRouter()

router.register(
    'record',
    RecordViewSet
)

urlpatterns = router.urls