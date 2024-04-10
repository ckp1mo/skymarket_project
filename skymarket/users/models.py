from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'null': True, 'blank': True}


class UserRoles(models.TextChoices):
    USER = 'user', 'пользователь'
    ADMIN = 'admin', 'администратор'


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name=_('Lastname'))
    phone = models.CharField(max_length=12, verbose_name=_('Номер телефона'))
    email = models.EmailField(unique=True, verbose_name='Email')
    role = models.CharField(max_length=5, choices=UserRoles.choices, default=UserRoles.USER)
    image = models.ImageField(upload_to='user/', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'role']

    def __str__(self):
        return f"{self.email}, {self.last_name}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
