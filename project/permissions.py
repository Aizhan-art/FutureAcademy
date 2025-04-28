from rest_framework.permissions import BasePermission

class OnlyReadForParentsPermission(BasePermission):
    """
    Разрешает только чтение для родителей, остальным полный доступ.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            return request.user.is_staff  # Только админам можно изменять
        return False