from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, DepartmentViewSet, DesignationViewSet, 
    EmployeeViewSet, AttendanceCheckInView, AttendanceCheckOutView,
    OrderAssignmentView
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'designations', DesignationViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('attendance/check-in/', AttendanceCheckInView.as_view(), name='attendance-check-in'),
    path('attendance/check-out/', AttendanceCheckOutView.as_view(), name='attendance-check-out'),
    path('orders/assign/', OrderAssignmentView.as_view(), name='order-assign'),
]
