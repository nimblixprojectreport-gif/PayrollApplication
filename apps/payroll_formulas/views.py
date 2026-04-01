from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import SalaryStructure, SalaryStructureVersion, SalaryComponent, PayrollFormula, SalaryStructureComponentMapping, EmployeeSalary
from .serializers import (
    SalaryStructureSerializer, SalaryStructureVersionSerializer, SalaryComponentSerializer,
    PayrollFormulaSerializer, SalaryStructureComponentMappingSerializer, EmployeeSalarySerializer,
)


class SalaryStructureListCreateView(generics.ListCreateAPIView):
    queryset = SalaryStructure.objects.all()
    serializer_class = SalaryStructureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company', 'is_active']


class SalaryStructureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalaryStructure.objects.all()
    serializer_class = SalaryStructureSerializer
    lookup_field = 'pk'


class SalaryStructureVersionListCreateView(generics.ListCreateAPIView):
    queryset = SalaryStructureVersion.objects.all()
    serializer_class = SalaryStructureVersionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['salary_structure']


class SalaryComponentListCreateView(generics.ListCreateAPIView):
    queryset = SalaryComponent.objects.all()
    serializer_class = SalaryComponentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company', 'component_type', 'is_active']


class SalaryComponentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalaryComponent.objects.all()
    serializer_class = SalaryComponentSerializer
    lookup_field = 'pk'


class PayrollFormulaListCreateView(generics.ListCreateAPIView):
    queryset = PayrollFormula.objects.all()
    serializer_class = PayrollFormulaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company']


class PayrollFormulaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PayrollFormula.objects.all()
    serializer_class = PayrollFormulaSerializer
    lookup_field = 'pk'


class SalaryStructureComponentMappingListCreateView(generics.ListCreateAPIView):
    queryset = SalaryStructureComponentMapping.objects.all()
    serializer_class = SalaryStructureComponentMappingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['salary_structure_version', 'salary_component']


class EmployeeSalaryListCreateView(generics.ListCreateAPIView):
    queryset = EmployeeSalary.objects.all()
    serializer_class = EmployeeSalarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee']


class EmployeeSalaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeSalary.objects.all()
    serializer_class = EmployeeSalarySerializer
    lookup_field = 'pk'
