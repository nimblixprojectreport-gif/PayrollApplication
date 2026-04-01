from rest_framework import serializers
from .models import SalaryStructure, SalaryStructureVersion, SalaryComponent, PayrollFormula, SalaryStructureComponentMapping, EmployeeSalary


class SalaryStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStructure
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SalaryStructureVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStructureVersion
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SalaryComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryComponent
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class PayrollFormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollFormula
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SalaryStructureComponentMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStructureComponentMapping
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class EmployeeSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSalary
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
