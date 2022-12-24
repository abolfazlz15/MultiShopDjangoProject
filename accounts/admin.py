from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, OTPCode
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


admin.site.register(User, UserAdmin)
admin.site.register(OTPCode)
