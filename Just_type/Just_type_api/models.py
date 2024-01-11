from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from djongo import models as md


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

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("is staff must be true for admin user"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("is superuser must be true for admin user"))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
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


class User_Errors(md.Model):
    userId = md.IntegerField()
    letters = md.JSONField()


class All_Words(md.Model):
    word = models.CharField(max_length=100)
    letters = md.JSONField()
