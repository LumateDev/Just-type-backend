from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
