from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'surname', 'is_staff')
    search_fields = ('email', 'name', 'surname')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('name', 'surname', 'phone', 'avatar', 'github_url', 'about')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login',)}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'phone', 'password'),
        }),
        )


admin.site.register(User, UserAdmin)
