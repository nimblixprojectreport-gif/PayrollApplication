from rest_framework import serializers
from .models import Attendance, Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class AttendanceCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['employee', 'latitude', 'longitude', 'selfie']

class AttendanceCheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id']
