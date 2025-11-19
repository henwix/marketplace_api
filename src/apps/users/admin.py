from django.contrib import admin

from src.apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser']
