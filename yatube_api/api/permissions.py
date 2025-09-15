from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Разрешить редактирование только автору объекта."""

    def has_permission(self, request, view):
        # безопасные запросы (GET, HEAD) доступны всем
        if request.method in SAFE_METHODS:
            return True
        # остальные методы — только для авторизованных
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # читать объект может любой пользователь
        if request.method in SAFE_METHODS:
            return True
        # а менять — только если он автор
        return getattr(obj, 'author', None) == request.user
