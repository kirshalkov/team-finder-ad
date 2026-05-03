from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from random import randint


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,
                              verbose_name='Почта')
    name = models.CharField(max_length=124,
                            verbose_name='Имя')
    surname = models.CharField(max_length=124,
                               verbose_name='Фамилия')
    phone = models.CharField(max_length=12,
                             verbose_name='Номер телефона',
                             blank=True, null=True)
    github_url = models.URLField(blank=True,
                                 null=True, verbose_name='Ссылка на github')
    about = models.TextField(max_length=256,
                             blank=True, null=True,
                             verbose_name='Описание профиля', default='')
    avatar = models.ImageField(upload_to='avatars/',
                               verbose_name='Аватар', blank=True)
    is_active = models.BooleanField(default=True,
                                    verbose_name='Активный пользователь')
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Администратор')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} {self.surname}'

    def generate_avatar(self, size=20):
        letter = self.name[0].upper()
        colors = [
            '#FF6B6B',
            '#4ECDC4',
            '#45B7D1',
            '#96CEB4',
            '#FFEAA7',
            '#DDA0DD',
            '#98D8C8',
            '#F7DC6F',
            '#BB8FCE',
            '#85C1E2',
            '#F8B88B',
            '#A8E6CF',
            '#FFD3B5',
            '#C7CEE6',
            '#FFB7B2',
        ]
        color_index = randint(0, len(colors)-1)
        bg_color = colors[color_index]
        img = Image.new('RGB', (size, size), bg_color)
        draw = ImageDraw.Draw(img)
        font_size = int(size * 0.7)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            print("Ошибка загрузки шрифта")
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size - text_width)//2, (size-text_height)//2)
        draw.text(position, letter, fill='white', font=font)

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return ContentFile(buffer.getvalue(), name=f'avatar_{self.pk}.png')

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            avatar_obj = self.generate_avatar()
            self.avatar = avatar_obj
        super().save(*args, **kwargs)
