from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Company, Department, Designation, Employee, Attendance, Order
from .serializers import (
    CompanySerializer, DepartmentSerializer, DesignationSerializer, 
    EmployeeSerializer, AttendanceSerializer, OrderSerializer,
    AttendanceCheckInSerializer, OrderAssignmentSerializer
)
from .utils import calculate_distance
from django.utils import timezone

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class AttendanceCheckInView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = AttendanceCheckInSerializer(data=request.data)
        if serializer.is_valid():
            employee = get_object_or_404(Employee, id=serializer.validated_data['employee_id'])
            attendance = Attendance.objects.create(
                employee=employee,
                latitude=serializer.validated_data['latitude'],
                longitude=serializer.validated_data['longitude'],
                selfie=serializer.validated_data.get('selfie')
            )
            return Response({"message": "Checked in successfully", "id": attendance.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendanceCheckOutView(APIView):
    def post(self, request):
        attendance_id = request.data.get('attendance_id')
        attendance = get_object_or_404(Attendance, id=attendance_id)
        if attendance.check_out:
            return Response({"message": "Already checked out"}, status=status.HTTP_400_BAD_REQUEST)
        
        attendance.check_out = timezone.now()
        attendance.save()
        return Response({"message": "Checked out successfully"}, status=status.HTTP_200_OK)

class OrderAssignmentView(APIView):
    def post(self, request):
        serializer = OrderAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            order = get_object_or_404(Order, id=order_id)
            
            if order.is_assigned:
                return Response({"message": "Order already assigned"}, status=status.HTTP_400_BAD_REQUEST)

            # Find all employees currently checked in at the same company
            active_attendances = Attendance.objects.filter(
                employee__company=order.company,
                check_out__isnull=True
            ).select_related('employee')

            if not active_attendances.exists():
                return Response({"message": "No active employees found for this company"}, status=status.HTTP_404_NOT_FOUND)

            nearest_employee = None
            min_distance = float('inf')

            for attendance in active_attendances:
                dist = calculate_distance(
                    order.latitude, order.longitude,
                    attendance.latitude, attendance.longitude
                )
                if dist < min_distance:
                    min_distance = dist
                    nearest_employee = attendance.employee

            if nearest_employee:
                order.assigned_employee = nearest_employee
                order.is_assigned = True
                order.save()
                return Response({
                    "message": "Order assigned based on proximity",
                    "employee_id": nearest_employee.id,
                    "employee_name": f"{nearest_employee.first_name} {nearest_employee.last_name}",
                    "distance_km": round(min_distance, 2)
                }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
