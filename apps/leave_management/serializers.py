from rest_framework import serializers
from .models import LeaveType

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = [
            'id', 
            'company', 
            'name', 
            'yearly_quota', 
            'carry_forward_allowed', 
            'max_carry_forward', 
            'is_paid_leave', 
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        """
        Check that max_carry_forward is 0 if carry_forward_allowed is False.
        """
        if not data.get('carry_forward_allowed') and data.get('max_carry_forward', 0) > 0:
            raise serializers.ValidationError({
                "max_carry_forward": "Max carry forward must be 0 if carry forward is not allowed."
            })
        return data
