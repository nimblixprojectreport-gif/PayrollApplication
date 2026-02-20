from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PayrollViewSet, PayrollItemViewSet, PayslipViewSet, FormulaViewSet

router = DefaultRouter()
router.register(r'payrolls', PayrollViewSet)
router.register(r'payroll-items', PayrollItemViewSet)
router.register(r'payslips', PayslipViewSet)
router.register(r'formulas', FormulaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
