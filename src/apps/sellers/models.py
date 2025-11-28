from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.common.models import TimedBaseModel
from src.apps.users.models import User


class Seller(TimedBaseModel):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='seller_profile')
    name = models.CharField(_('name'), max_length=100, help_text=_('Seller name'))
    description = models.TextField(_('description'), blank=True, null=True, help_text=_('Seller description'))
    avatar = models.CharField(_('avatar'), max_length=255, blank=True, null=True, help_text=_('Seller avatar'))
    background = models.CharField(
        _('background'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Seller background image'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'
