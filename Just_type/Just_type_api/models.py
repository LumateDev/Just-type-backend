from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Users must have an password.')

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'


class User_Data(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bestWPM = models.IntegerField(default=None)
    averageWPM = models.IntegerField(default=None)
    total_tests = models.IntegerField(default=None)

    class Meta:
        verbose_name_plural = 'Статистика пользователей'
        verbose_name = 'Статистика пользователя'


class User_Experience(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    experience = models.IntegerField(default=None)
    level = models.IntegerField(default=None)

    class Meta:
        verbose_name_plural = 'Статистика пользователей'
        verbose_name = 'Статистика пользователя'


class User_Errors(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    letters = models.JSONField()


class All_Words(models.Model):
    word = models.CharField(max_length=100)
    letters = models.JSONField()
