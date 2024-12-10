# backend/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Specify the fields to be displayed in the admin panel
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_of_birth', 'deleted_at')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_of_birth')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('deleted_at',)

    # Define the form fields for creating/editing users
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'deleted_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    # Override the save method to handle soft deletion if necessary
    def save_model(self, request, obj, form, change):
        if obj.deleted_at:
            obj.soft_delete()
        else:
            super().save_model(request, obj, form, change)

# Register the User model with the custom UserAdmin
admin.site.register(User, UserAdmin)
