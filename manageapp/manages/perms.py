from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Chỉ cho phép admin thay đổi, còn user thường chỉ được xem (GET).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Chủ sở hữu (resident) của object hoặc admin mới được sửa/xoá.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.resident == request.user
