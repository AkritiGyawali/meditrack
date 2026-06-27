from rest_framework.permissions import BasePermission


class IsAdminForDelete(BasePermission):
    """Allow delete only for staff/admin users."""
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_staff or request.user.groups.filter(name='admin').exists()
        return True


class CanManageAppointments(BasePermission):
    """Only doctors, receptionists, and admins can create/update appointments."""
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH']:
            return request.user.groups.filter(
                name__in=['doctor', 'receptionist', 'admin']
            ).exists() or request.user.is_staff
        return True


class IsAdminOnly(BasePermission):
    """Only admins can access this endpoint."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='admin').exists() or request.user.is_staff

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_filter(
            name='Doctor'
        ).exists():
            return True