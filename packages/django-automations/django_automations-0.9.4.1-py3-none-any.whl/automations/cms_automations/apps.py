# coding=utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CmsAutomationsConfig(AppConfig):
    name = "automations.cms_automations"
    default_auto_field = "django.db.models.AutoField"
    verbose_name = _("CMS Automations")
