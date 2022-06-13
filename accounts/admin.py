from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from accounts.models import MinhotecaUser


@admin.register(MinhotecaUser)
class MinhotecaUserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {'fields': (
            'is_active', 'email_confirmed', 'is_staff',
            'is_superuser', 'groups', 'user_permissions'
        )}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_active', 'email_confirmed', 'date_joined')
    search_fields = ('email',)
    ordering = ('email',)
