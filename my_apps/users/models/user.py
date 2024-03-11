from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, phone, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        if not email:
            raise ValueError(_('The Email field must be set'))
        if not phone:
            raise ValueError(_('The Phone field must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, name=name, password=password, **extra_fields)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, phone, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None

    email = models.EmailField(_('Email'), unique=True)
    phone = PhoneNumberField(_('Phone'), unique=True, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        super().save(*args, **kwargs)
