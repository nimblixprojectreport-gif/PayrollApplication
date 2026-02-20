from rest_framework import generics
from .models import LeaveType
from .serializers import LeaveTypeSerializer

class LeaveTypeListCreateView(generics.ListCreateAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned leave types to a given company,
        by filtering against a `company_id` query parameter in the URL.
        """
        queryset = LeaveType.objects.all()
        company_id = self.request.query_params.get('company_id')
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        return queryset
