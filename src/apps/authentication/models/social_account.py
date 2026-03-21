from django.contrib.postgres.indexes import Index
from django.db import models

from src.apps.authentication.constants import SocialAccountProviders
from src.apps.common.models import TimedBaseModel
from src.apps.users.models import User


class SocialAccount(TimedBaseModel):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='social_accounts',
        verbose_name='user',
    )
    provider = models.CharField(
        max_length=32,
        choices=SocialAccountProviders.choices,
        verbose_name='provider name',
    )
    provider_uid = models.CharField(
        verbose_name='provider uid',
    )

    def __str__(self):
        return f'{self.provider} social account for User #{self.user_id}'

    class Meta:
        verbose_name = 'Social account'
        verbose_name_plural = 'Social accounts'
        constraints = [
            models.UniqueConstraint(fields=['user', 'provider'], name='unique_user_provider'),
            models.UniqueConstraint(fields=['provider_uid', 'provider'], name='unique_provider_uid'),
        ]
        indexes = [
            Index(fields=['provider_uid', 'provider']),
        ]
