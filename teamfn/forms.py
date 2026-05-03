from django import forms

from core.mixins import GithubValidationMixin
from teamfn.models import Project


class ProjectForm(GithubValidationMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название проекта'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-area',
                'placeholder': 'Опишите ваш проект',
                'rows': 5
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://github.com/user/repo'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
