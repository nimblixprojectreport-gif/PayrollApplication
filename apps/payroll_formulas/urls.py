from django.urls import path
from .views import (
    SalaryStructureListCreateView, SalaryStructureDetailView,
    SalaryStructureVersionListCreateView,
    SalaryComponentListCreateView, SalaryComponentDetailView,
    PayrollFormulaListCreateView, PayrollFormulaDetailView,
    SalaryStructureComponentMappingListCreateView,
    EmployeeSalaryListCreateView, EmployeeSalaryDetailView,
)

urlpatterns = [
    path('salary-structures/', SalaryStructureListCreateView.as_view(), name='salary-structure-list'),
    path('salary-structures/<str:pk>/', SalaryStructureDetailView.as_view(), name='salary-structure-detail'),
    path('salary-structure-versions/', SalaryStructureVersionListCreateView.as_view(), name='salary-version-list'),
    path('salary-components/', SalaryComponentListCreateView.as_view(), name='salary-component-list'),
    path('salary-components/<str:pk>/', SalaryComponentDetailView.as_view(), name='salary-component-detail'),
    path('payroll-formulas/', PayrollFormulaListCreateView.as_view(), name='payroll-formula-list'),
    path('payroll-formulas/<str:pk>/', PayrollFormulaDetailView.as_view(), name='payroll-formula-detail'),
    path('salary-component-mappings/', SalaryStructureComponentMappingListCreateView.as_view(), name='salary-component-mapping-list'),
    path('employee-salaries/', EmployeeSalaryListCreateView.as_view(), name='employee-salary-list'),
    path('employee-salaries/<str:pk>/', EmployeeSalaryDetailView.as_view(), name='employee-salary-detail'),
]
