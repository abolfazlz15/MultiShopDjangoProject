from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User, UserAddress


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # permissions
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if not request.user.is_superuser:
            if db_field.name == 'is_superuser' or db_field.name == 'is_admin':
                field.widget = forms.HiddenInput()
        return field

    def has_change_permission(self, request, obj=None):
        if obj is not None and request.user.is_superuser == False:
            if obj is not None and request.user != obj:
                if obj is not None and request.user.is_admin and obj.is_admin:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and request.user.is_superuser == False:
            if obj is not None and request.user.is_admin and obj.is_admin:
                return False
            else:
                return True
        else:
            return True

    list_display = ('showImage', 'phone', 'email', 'full_name', 'is_admin')
    list_filter = ('is_admin', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('email', 'full_name', 'profile_image')}),
        ('Permissions', {'fields': ('is_superuser', 'is_admin', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'phone', 'full_name')
    ordering = ('full_name',)
    list_display_links = ('showImage', 'phone', 'email', 'full_name', 'is_admin')
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(UserAddress)
