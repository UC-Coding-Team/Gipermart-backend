from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PaymartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.paymart'
    verbose_name = _('paymart')
