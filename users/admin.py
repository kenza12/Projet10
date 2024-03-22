from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin class to manage User models in the Django admin interface.
    """
    model = User
     # Additional fields for User in the admin form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', 'can_be_contacted', 'can_data_be_shared')}),
    )
    # Additional fields when adding a new User
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('age', 'can_be_contacted', 'can_data_be_shared')}),
    )
    # Display these fields in the User list page
    list_display = ['username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared']
