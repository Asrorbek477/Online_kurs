from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsInstructor(BasePermission):
    """
    Faqat is_instructor=True bo'lgan foydalanuvchilarga ruxsat beradi.
    """
    message = "Bu amalni faqat instruktorlar bajarishi mumkin."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_instructor
        )


class IsOwnerOrAdmin(BasePermission):
    """
    Ob'ektga faqat egasi yoki admin kira oladi.
    Masalan: foydalanuvchi faqat o'z profilini o'zgartira oladi.
    """
    message = "Siz faqat o'z ma'lumotlaringizni o'zgartira olasiz."

    def has_object_permission(self, request, view, obj):
        # O'qish so'rovlarida (GET) hamma kira oladi
        if request.method in SAFE_METHODS:
            return True
        # Yozishda faqat egasi yoki admin
        return obj == request.user or request.user.is_staff