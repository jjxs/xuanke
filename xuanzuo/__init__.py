from django.apps import AppConfig
import os

VERBOSE_APP_NAME = u"选座系统"


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class PrimaryBlogConfig(AppConfig):
    name = VERBOSE_APP_NAME
    verbose_name = VERBOSE_APP_NAME