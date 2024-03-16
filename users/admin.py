from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', 'can_be_contacted', 'can_data_be_shared')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('age', 'can_be_contacted', 'can_data_be_shared')}),
    )
    list_display = ['username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared']
