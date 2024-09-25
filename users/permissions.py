from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором и регулирует доступ к действиям.
    """

    def has_permission(self, request, view):
        is_moder = request.user.groups.filter(name="moders").exists()

        # Модераторам разрешаем только безопасные методы и обновление (PUT, PATCH)
        if is_moder:
            if request.method in permissions.SAFE_METHODS or request.method in [
                "PUT",
                "PATCH",
            ]:
                return True
            # Запрещаем создание (POST) и удаление (DELETE) для модераторов
            return False

        # Разрешаем действия для всех других пользователей
        return True


class IsOwner(permissions.BasePermission):
    """
    Проверяет, что пользователь является владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
