from django.conf import settings
from rest_framework import permissions


class HasAccessToken(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.DATA.get('access_token') == settings.ACCESS_TOKEN:
            return True
        return False


class HasAccessTokenOrLoggedIn(HasAccessToken):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated()
        return super(HasAccessTokenOrLoggedIn, self).has_permission(request, view)
