from io import BytesIO

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from core.constants import (
    AVATAR_FONT_RATIO, AVATAR_SIZE, AVATAR_TEXT_COLOR,
    AvatarColor, MAX_LENGTH_ABOUT, MAX_LENGTH_PHONE,
    MAX_LENGTH_STANDARD, TEXT_ANCHOR_COORDS, TEXT_VERTICAL_OFFSET
)

from users.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name='Почта'
    )
    name = models.CharField(
        max_length=MAX_LENGTH_STANDARD,
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=MAX_LENGTH_STANDARD,
        verbose_name='Фамилия'
    )
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        verbose_name='Номер телефона',
        blank=True,
        null=True
    )
    github_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на github'
    )
    about = models.TextField(
        max_length=MAX_LENGTH_ABOUT,
        blank=True,
        null=True,
        verbose_name='Описание профиля',
        default=''
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        verbose_name='Аватар',
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный пользователь'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Администратор'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            self.avatar = self.generate_avatar()
        super().save(*args, **kwargs)

    def generate_avatar(self, size=AVATAR_SIZE):
        letter = self.name[0].upper()
  
        bg_color = AvatarColor.get_random()

        img = Image.new('RGB', (size, size), bg_color)
        draw = ImageDraw.Draw(img)

        font_size = int(size * AVATAR_FONT_RATIO)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        bbox = draw.textbbox(TEXT_ANCHOR_COORDS,
                             letter, font=font)

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = (
            (size - text_width) // 2,
            (size - text_height) // 2 - TEXT_VERTICAL_OFFSET)
        draw.text(position, letter, fill=AVATAR_TEXT_COLOR, font=font)

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        return ContentFile(
            buffer.getvalue(),
            name=f'avatar_{self.pk}.png'
        )
