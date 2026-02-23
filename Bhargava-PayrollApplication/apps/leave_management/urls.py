from django.urls import path
from .views import (
    LeaveTypeListView, 
    LeaveTypeListCreateView, 
    LeaveRequestApproveView, 
    LeaveRequestRejectView, 
    EmployeeLeaveBalanceView
)

urlpatterns = [
    path('leave-types', LeaveTypeListView.as_view(), name='leave-type-list-create'),
    path('leave-requests', LeaveTypeListCreateView.as_view(), name='leave-request-list-create'),
    path('leave-requests/<uuid:pk>/approve', LeaveRequestApproveView.as_view(), name='leave-request-approve'),
    path('leave-requests/<uuid:pk>/reject', LeaveRequestRejectView.as_view(), name='leave-request-reject'),
    path('employees/<uuid:employee_id>/leave-balance', EmployeeLeaveBalanceView.as_view(), name='employee-leave-balance'),
]
