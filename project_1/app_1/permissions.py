from rest_framework import permissions
from django.contrib.auth.models import User
class CustomPermissionTEST(permissions.BasePermission):

    def _get_admin(self)->tuple:
        '''
        я так пока что и не понял почему  этот метод вызывается 6 раз
        '''
        users = User.objects.filter(is_staff=True)
        return (user.username for user in users)

    def has_permission(self, request, view):
        users = self._get_admin()
        if request.user.username in users:
            return True
        elif request.method in permissions.SAFE_METHODS or request.method in 'POST':
            return True