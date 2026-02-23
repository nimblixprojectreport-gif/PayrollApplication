from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import LeaveType, LeaveRequest, LeaveBalance
from .serializers import LeaveTypeSerializer, LeaveRequestSerializer, LeaveBalanceSerializer
from apps.employees.models import Employee

class LeaveTypeListCreateView(generics.ListCreateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer

class LeaveRequestApproveView(APIView):
    def put(self, request, pk):
        try:
            leave_request = LeaveRequest.objects.get(pk=pk)
        except LeaveRequest.DoesNotExist:
            return Response({"error": "Leave request not found"}, status=status.HTTP_404_NOT_FOUND)

        if leave_request.status != 'Pending':
            return Response({"error": "Only pending requests can be approved"}, status=status.HTTP_400_BAD_REQUEST)

        leave_request.status = 'Approved'
        leave_request.approved_at = timezone.now()
        
        # Try to set approved_by to the current user's employee record
        try:
            if hasattr(request.user, 'employee'):
                leave_request.approved_by = request.user.employee
        except Exception:
            pass
        
        leave_request.save()

        # Update Leave Balance
        current_year = timezone.now().year
        balance, created = LeaveBalance.objects.get_or_create(
            employee_id=leave_request.employee_id,
            leave_type_id=leave_request.leave_type_id,
            year=current_year,
            defaults={'allocated': leave_request.leave_type_id.yearly_quota, 'used': 0}
        )
        
        balance.used += int(leave_request.total_days)
        balance.save()

        return Response(LeaveRequestSerializer(leave_request).data)

class LeaveRequestRejectView(APIView):
    def put(self, request, pk):
        try:
            leave_request = LeaveRequest.objects.get(pk=pk)
        except LeaveRequest.DoesNotExist:
            return Response({"error": "Leave request not found"}, status=status.HTTP_404_NOT_FOUND)

        if leave_request.status != 'Pending':
            return Response({"error": "Only pending requests can be rejected"}, status=status.HTTP_400_BAD_REQUEST)

        leave_request.status = 'Rejected'
        leave_request.save()

        return Response(LeaveRequestSerializer(leave_request).data)

class EmployeeLeaveBalanceView(APIView):
    def get(self, request, employee_id):
        current_year = timezone.now().year
        balances = LeaveBalance.objects.filter(employee_id_id=employee_id, year=current_year)
        serializer = LeaveBalanceSerializer(balances, many=True)
        return Response(serializer.data)

class LeaveTypeListView(generics.ListCreateAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer

    def get_queryset(self):
        queryset = LeaveType.objects.all()
        company_id = self.request.query_params.get('company_id')
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        return queryset
