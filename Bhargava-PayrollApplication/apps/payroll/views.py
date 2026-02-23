from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
import calendar
from datetime import datetime

from .models import (
    Payroll, PayrollItem, PayrollItemComponent, 
    PayrollFormula, Payslip, SalaryStructure, 
    SalaryStructureComponent, EmployeeSalaryStructure
)
from .serializers import (
    PayrollSerializer, PayrollItemSerializer, PayrollItemComponentSerializer,
    PayrollFormulaSerializer, PayslipSerializer, SalaryStructureSerializer
)
from apps.employees.models import Employee
from apps.attendance.models import Attendance
from apps.leave_management.models import LeaveRequest

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer

    @action(detail=False, methods=['post'])
    def generate(self, request):
        company_id = request.data.get('company_id')
        month = int(request.data.get('month'))
        year = int(request.data.get('year'))
        generated_by_id = request.data.get('generated_by')

        if not all([company_id, month, year]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Fetch Company and Employees
        employees = Employee.objects.filter(company_id=company_id, is_active=True)
        if not employees.exists():
            return Response({"error": "No active employees found"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Create Payroll Record
            payroll = Payroll.objects.create(
                company_id=company_id,
                month=month,
                year=year,
                status='Draft',
                generated_by_id=generated_by_id,
                total_employees=employees.count()
            )

            total_gross = 0
            total_deductions = 0
            total_net = 0

            for employee in employees:
                # 2. Fetch Attendance
                num_days = calendar.monthrange(year, month)[1]
                attendance_count = Attendance.objects.filter(
                    employee=employee,
                    date__month=month,
                    date__year=year
                ).count()
                
                # 3. Fetch Approved Leaves
                leave_days = LeaveRequest.objects.filter(
                    employee_id_id=employee.id,
                    status='Approved',
                    start_date__month=month,
                    start_date__year=year
                ).aggregate(total=Sum('total_days'))['total'] or 0
                
                # Simplified calculation
                working_days = num_days
                present_days = attendance_count
                lop_days = max(0, working_days - (present_days + leave_days))
                payable_days = working_days - lop_days

                # 4. Fetch Salary Structure
                try:
                    emp_salary_struct = EmployeeSalaryStructure.objects.get(employee=employee)
                    salary_structure = emp_salary_struct.salary_structure
                except EmployeeSalaryStructure.DoesNotExist:
                    continue # Skip employees without salary structure

                # 5. Create Payroll Item
                payroll_item = PayrollItem.objects.create(
                    payroll=payroll,
                    employee=employee,
                    working_days=working_days,
                    present_days=present_days,
                    leave_days=leave_days,
                    lop_days=lop_days,
                    payable_days=payable_days
                )

                item_gross = 0
                item_deductions = 0

                # 6. Calculate Components (Simplified)
                # Base salary is adjusted by payable days
                base_amount = (emp_salary_struct.base_salary / working_days) * payable_days
                
                # Process Earning/Deduction components
                for comp in salary_structure.components.all():
                    comp_amount = comp.amount # Simplified: ignoring complex formulas for now
                    if comp.component_type == 'Earning':
                        item_gross += comp_amount
                    else:
                        item_deductions += comp_amount
                    
                    PayrollItemComponent.objects.create(
                        payroll_item=payroll_item,
                        component_name=comp.name,
                        component_type=comp.component_type,
                        amount=comp_amount
                    )

                # Add base salary as a component
                PayrollItemComponent.objects.create(
                    payroll_item=payroll_item,
                    component_name="Base Salary",
                    component_type="Earning",
                    amount=base_amount
                )
                item_gross += base_amount

                payroll_item.gross_salary = item_gross
                payroll_item.total_deductions = item_deductions
                payroll_item.net_salary = item_gross - item_deductions
                payroll_item.save()

                total_gross += item_gross
                total_deductions += item_deductions
                total_net += payroll_item.net_salary

            # Update Payroll totals
            payroll.total_gross = total_gross
            payroll.total_deductions = total_deductions
            payroll.total_net = total_net
            payroll.save()

        return Response(PayrollSerializer(payroll).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def finalize(self, request, pk=None):
        payroll = self.get_object()
        if payroll.status == 'Finalized':
            return Response({"error": "Payroll already finalized"}, status=status.HTTP_400_BAD_REQUEST)
        
        payroll.status = 'Finalized'
        payroll.finalized_at = timezone.now()
        payroll.locked = True
        payroll.save()
        return Response(PayrollSerializer(payroll).data)

class PayrollItemViewSet(viewsets.ModelViewSet):
    queryset = PayrollItem.objects.all()
    serializer_class = PayrollItemSerializer

    @action(detail=True, methods=['put'])
    def mark_paid(self, request, pk=None):
        item = self.get_object()
        item.is_paid = True
        item.paid_date = request.data.get('paid_date', timezone.now().date())
        item.payment_reference = request.data.get('payment_reference')
        item.save()
        return Response(PayrollItemSerializer(item).data)

class PayslipViewSet(viewsets.ModelViewSet):
    queryset = Payslip.objects.all()
    serializer_class = PayslipSerializer

    @action(detail=False, methods=['post'])
    def generate(self, request):
        payroll_item_id = request.data.get('payroll_item_id')
        try:
            payroll_item = PayrollItem.objects.get(id=payroll_item_id)
        except PayrollItem.DoesNotExist:
            return Response({"error": "Payroll item not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate a unique payslip number
        payslip_number = f"PS-{payroll_item.payroll.year}{payroll_item.payroll.month:02d}-{payroll_item.id.hex[:6]}"
        
        payslip, created = Payslip.objects.get_or_create(
            payroll_item=payroll_item,
            defaults={'payslip_number': payslip_number}
        )
        
        return Response(PayslipSerializer(payslip).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        payslip = self.get_object()
        # Mock download path - in real app, this would return a PDF file
        return Response({
            "message": "Downloading payslip",
            "payslip_number": payslip.payslip_number,
            "file_url": f"/media/payslips/{payslip.payslip_number}.pdf"
        })

class FormulaViewSet(viewsets.ModelViewSet):
    queryset = PayrollFormula.objects.all()
    serializer_class = PayrollFormulaSerializer
