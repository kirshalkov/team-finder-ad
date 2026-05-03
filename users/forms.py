import re

from django import forms
from django.contrib.auth import authenticate, get_user_model

from core.mixins import GithubValidationMixin


User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError('Неправильная почта или пароль!')
            self.user_cache = user
        return cleaned_data


class ProfileEditForm(GithubValidationMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'avatar', 'about', 'phone', 'github_url')
        widgets = {'avatar': forms.FileInput(attrs={
            'class': 'hidden-avatar-input', 'id': 'id_avatar'})}

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        if phone.startswith('8'):
            phone = '+7' + phone[1:]
        if not re.fullmatch(r'\+7\d{10}', phone):
            raise forms.ValidationError(
                'Номер должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX'
            )
        if User.objects.filter(phone=phone).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                'Пользователь с таким номером уже существует'
            )
        return phone


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label='Подтвердите новый пароль',
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Неверный текущий пароль')
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password2 and new_password1 and new_password1 != new_password2:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data
