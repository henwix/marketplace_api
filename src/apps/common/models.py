from django.db import models
from django.utils.translation import gettext_lazy as _


class TimedBaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True,
        help_text=_('Date of creation'),
    )
    updated_at = models.DateTimeField(
        verbose_name=_('updated at'),
        auto_now=True,
        help_text=_('Date of update'),
    )

    class Meta:
        abstract = True
