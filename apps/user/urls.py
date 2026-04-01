from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    RoleListCreateView, RoleDetailView,
    PermissionListCreateView, PermissionDetailView,
    RolePermissionListCreateView,
    UserRoleListCreateView,
)

urlpatterns = [
    # Users
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<str:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Roles
    path('roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('roles/<str:pk>/', RoleDetailView.as_view(), name='role-detail'),

    # Permissions
    path('permissions/', PermissionListCreateView.as_view(), name='permission-list-create'),
    path('permissions/<str:pk>/', PermissionDetailView.as_view(), name='permission-detail'),

    # Role-Permission assignments
    path('role-permissions/', RolePermissionListCreateView.as_view(), name='role-permission-list'),

    # User-Role assignments
    path('user-roles/', UserRoleListCreateView.as_view(), name='user-role-list'),
]
