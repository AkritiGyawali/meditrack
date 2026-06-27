from rest_framework.permissions import BasePermission


class IsAdminForDelete(BasePermission):
    """Allow delete only for staff/admin users."""
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_staff or request.user.groups.filter(name='admin').exists()
        return True


class IsDoctorOrAdmin(BasePermission):
    """Only doctors and admins can access doctor endpoints."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['doctor', 'admin']).exists() or request.user.is_staff


class IsAdminOnly(BasePermission):
    """Only admins can access this endpoint."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='admin').exists() or request.user.is_staff