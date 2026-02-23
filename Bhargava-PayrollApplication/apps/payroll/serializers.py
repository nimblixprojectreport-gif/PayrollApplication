from rest_framework import serializers
from .models import (
    Payroll, PayrollItem, PayrollItemComponent, 
    PayrollFormula, Payslip, SalaryStructure, SalaryStructureComponent
)

class SalaryStructureComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStructureComponent
        fields = '__all__'

class SalaryStructureSerializer(serializers.ModelSerializer):
    components = SalaryStructureComponentSerializer(many=True, read_only=True)
    class Meta:
        model = SalaryStructure
        fields = '__all__'

class PayrollItemComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollItemComponent
        fields = '__all__'

class PayrollItemSerializer(serializers.ModelSerializer):
    components = PayrollItemComponentSerializer(many=True, read_only=True)
    class Meta:
        model = PayrollItem
        fields = '__all__'

class PayrollSerializer(serializers.ModelSerializer):
    items = PayrollItemSerializer(many=True, read_only=True)
    items_count = serializers.IntegerField(source='items.count', read_only=True)
    class Meta:
        model = Payroll
        fields = '__all__'

class PayrollFormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollFormula
        fields = '__all__'

class PayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip
        fields = '__all__'
