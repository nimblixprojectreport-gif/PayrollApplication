from django.urls import path
from .views import LeaveTypeListCreateView

urlpatterns = [
    path('leave-types/', LeaveTypeListCreateView.as_view(), name='leave-type-list-create'),
]
