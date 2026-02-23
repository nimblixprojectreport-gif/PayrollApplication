from django.urls import path
from .views import DepartmentListCreateAPIView

urlpatterns = [
    path('Departments/', DepartmentListCreateAPIView.as_view(), name='Departments'),
]