from rest_framework import permissions


class IsSuperAdminOrManager(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_super_admin or\
            obj.id == request.user.id or\
            request.user == obj.manager
