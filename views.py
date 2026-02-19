from rest_framework import viewsets
from .models import LeaveBalance, LeaveRequest
from .serializers import LeaveBalanceSerializer, LeaveRequestSerializer


class LeaveBalanceViewSet(viewsets.ModelViewSet):
    queryset = LeaveBalance.objects.all()
    serializer_class = LeaveBalanceSerializer


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
