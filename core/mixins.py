from django import forms

from core.constants import ALLOWED_HOSTS_VALIDATION

class GithubValidationMixin:

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and ALLOWED_HOSTS_VALIDATION not in url.lower():
            raise forms.ValidationError('Ссылка должна вести на GitHub')
        return url
