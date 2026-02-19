from rest_framework import serializers
from .models import LeaveBalance, LeaveRequest


class LeaveBalanceSerializer(serializers.ModelSerializer):
    remaining_leaves = serializers.IntegerField(source='remaining_leaves', read_only=True)

    class Meta:
        model = LeaveBalance
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'
