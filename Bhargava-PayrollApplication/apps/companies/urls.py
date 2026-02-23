from django.urls import path
from .views import (
    CompanyListCreateView, 
    CompanySettingsListCreateView, 
    CompanySettingsDetailView
)

urlpatterns = [
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('company-settings/', CompanySettingsListCreateView.as_view(), name='company-settings-list-create'),
    path('companies/<uuid:company_id>/settings/', CompanySettingsDetailView.as_view(), name='company-settings-detail'),
]
