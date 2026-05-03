from .models import Project
from django import forms


class ProjectForm(forms.ModelForm):

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

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and 'github.com' not in url.lower():
            raise forms.ValidationError('Ссылка должна вести на github')
        return url