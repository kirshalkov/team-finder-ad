from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'name',
        'surname',
        'is_staff',
        'projects_count'
    )
    search_fields = ('email', 'name', 'surname')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {
            'fields': (
                'name',
                'surname',
                'phone',
                'avatar',
                'github_url',
                'about',
            )
        }),
        ('Права доступа', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Даты', {'fields': ('last_login',)}),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            projects_count=Count('participated_projects')
        )

    @admin.display(description='Кол-во проектов', ordering='projects_count')
    def projects_count(self, obj):
        return obj.projects_count
