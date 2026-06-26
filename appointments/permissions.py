from rest_framework.permissions  import BasePermission

class IsAdminForDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_staff
        return True

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_filter(
            name='Doctor'
        ).exists():
            return True