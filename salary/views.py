from django.shortcuts import render

from rest_framework import viewsets
from .models import SalaryComponent, SalaryStructure
from .serializers import (
    SalaryComponentSerializer,
    SalaryStructureSerializer
)


class SalaryComponentViewSet(viewsets.ModelViewSet):
    queryset = SalaryComponent.objects.all()
    serializer_class = SalaryComponentSerializer


class SalaryStructureViewSet(viewsets.ModelViewSet):
    queryset = SalaryStructure.objects.all()
    serializer_class = SalaryStructureSerializer

# Create your views here.
