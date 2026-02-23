from rest_framework import generics
from .models import Company, CompanySettings
from .serializers import CompanySerializer, CompanySettingsSerializer

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanySettingsListCreateView(generics.ListCreateAPIView):
    queryset = CompanySettings.objects.all()
    serializer_class = CompanySettingsSerializer

class CompanySettingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanySettings.objects.all()
    serializer_class = CompanySettingsSerializer
    lookup_field = 'company_id'
