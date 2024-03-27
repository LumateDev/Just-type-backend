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


class UserData(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    best_WPM = models.FloatField(default=None)
    average_WPM = models.FloatField(default=None)
    tests_count = models.IntegerField(default=None)
    average_accuracy = models.FloatField(default=None)
    best_accuracy = models.FloatField(default=None)

    class Meta:
        verbose_name_plural = 'Статистика пользователей'
        verbose_name = 'Статистика пользователя'


class UserExperience(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, db_column='user_id')
    experience = models.FloatField(default=None)
    level = models.IntegerField(default=None)

    class Meta:
        verbose_name_plural = 'Статистика пользователей'
        verbose_name = 'Статистика пользователя'


class UserErrors(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, db_column="user_id")
    letters = models.JSONField()


class AllWords(models.Model):
    word = models.CharField(max_length=100)
    letters = models.JSONField()
