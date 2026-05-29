from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_instructor', 'is_staff']
    list_filter = ['is_instructor', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha', {'fields': ('is_instructor',)}),
    )