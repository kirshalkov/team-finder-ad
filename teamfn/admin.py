from django.contrib import admin

from teamfn.models import Project, Skill


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'skills')
    search_fields = ('name', 'owner__email', 'owner__surname', 'description')
    ordering = ('-created_at',)
    list_editable = ('status',)

    fieldsets = (
        (None, {
            'fields': ('name', 'status')
        }),
        ('Описание проекта', {
            'fields': ('description', 'github_url')
        }),
        ('Управление командой', {
            'fields': ('owner', 'participants'),
            'description': 'Владелец проекта и текущий состав участников'
        }),
        ('Навыки', {
            'fields': ('skills',),
        }),
    )

    filter_horizontal = ('participants', 'skills')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
