"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.authentication.urls")),
    path("api/v1/companies/", include("apps.companies.urls")),
    path("api/v1/users/", include("apps.user.urls")),
    path("api/v1/organization/", include("apps.organization.urls")),
    path("api/v1/employees/", include("apps.employees.urls")),
    path("api/v1/salary/", include("apps.payroll_formulas.urls")),
    path("api/v1/attendance/", include("apps.attendance_app.urls")),
    path("api/v1/leave/", include("apps.leave_management.urls")),
    path("api/v1/payroll/", include("apps.payroll.urls")),
    path("api/v1/audit/", include("apps.audit.urls")),
]
