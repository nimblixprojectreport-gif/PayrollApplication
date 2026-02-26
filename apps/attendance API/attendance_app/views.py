from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Attendance, Employee
from .serializers import AttendanceCheckInSerializer, AttendanceCheckOutSerializer, EmployeeSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class CheckInView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = AttendanceCheckInSerializer(data=request.data)
        if serializer.is_valid():
            attendance = serializer.save()
            return Response({
                "message": "Checked in successfully",
                "attendance_id": attendance.id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckOutView(APIView):
    def post(self, request, *args, **kwargs):
        attendance_id = request.data.get('attendance_id')
        if not attendance_id:
            return Response({"error": "attendance_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            attendance = Attendance.objects.get(id=attendance_id)
            if attendance.check_out_time:
                return Response({"message": "Already checked out"}, status=status.HTTP_400_BAD_REQUEST)
            
            attendance.check_out_time = timezone.now()
            attendance.save()
            return Response({"message": "Checked out successfully"}, status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response({"error": "Attendance record not found"}, status=status.HTTP_404_NOT_FOUND)
