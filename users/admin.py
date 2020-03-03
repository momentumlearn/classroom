from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Team, User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        'email',
    ]

    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_type', 'team')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
    )
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Team)
