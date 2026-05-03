from django.db import models
from django.contrib.auth import get_user_model


user_model = get_user_model()


class Project(models.Model):

    class ProjectStatus(models.TextChoices):
        OPEN = 'open', 'Открыт'
        CLOSE = 'closed', 'Закрыт'

    name = models.CharField(
        max_length=200,
        verbose_name='Название проекта'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    owner = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='owned_projects'
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    github_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на проект'
    )
    status = models.CharField(
        choices=ProjectStatus.choices,
        max_length=6,
        default=ProjectStatus.OPEN,
        verbose_name='Статус проекта'
    )
    participants = models.ManyToManyField(
        user_model,
        related_name='participated_projects',
        verbose_name='Участники проекта',
        blank=True
    )
    skills = models.ManyToManyField(
        'Skill',
        related_name='projects',
        verbose_name='Навыки',
        blank=True
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(
        max_length=124,
        verbose_name='Навык'
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name
