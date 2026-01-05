from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.apps.users.managers import CustomUserManager
from src.apps.users.validators import user_phone_validator


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=150,
        help_text=_('First name'),
    )
    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=150,
        help_text=_('Last name'),
    )
    email = models.EmailField(
        verbose_name=_('email address'),
        unique=True,
        help_text=_('Email'),
    )
    phone = models.CharField(
        verbose_name=_('phone number'),
        validators=[user_phone_validator],
        unique=True,
        max_length=20,
        help_text=_('Phone number'),
    )
    password = models.CharField(
        verbose_name=_('password'),
        max_length=128,
        help_text=_('Password'),
    )
    avatar = models.CharField(
        verbose_name=_('avatar'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('Avatar'),
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.',
        ),
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        verbose_name=_('date joined'),
        default=timezone.now,
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
