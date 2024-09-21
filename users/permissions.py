from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором, и запрещает удаление и создание.
    """

    def has_permission(self, request, view):
        # Проверяем, является ли пользователь частью группы "moders"
        is_moder = request.user.groups.filter(name="moders").exists()
        # Разрешаем только безопасные методы (GET, HEAD, OPTIONS) или обновление (PUT, PATCH)
        if is_moder and request.method in permissions.SAFE_METHODS:
            return True
        if is_moder and request.method in ["PUT", "PATCH"]:
            return True
        # Запрещаем создание (POST) и удаление (DELETE)
        if request.method in ["POST", "DELETE"]:
            return False
        return False


class IsOwner(permissions.BasePermission):
    """
    Проверяем что пользователь владелец.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
