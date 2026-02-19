from rest_framework.routers import DefaultRouter
from .views import LeaveBalanceViewSet, LeaveRequestViewSet

router = DefaultRouter()
router.register(r'leave-balances', LeaveBalanceViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)

urlpatterns = router.urls
