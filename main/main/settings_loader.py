from django.apps import apps
from django.db.utils import OperationalError

def get_theme_name():
    if apps.ready:
        try:
            from setup.models import ThemeSettings
            theme_name = ThemeSettings.objects.get().name
            return 'core/theme/' + theme_name + '/views'
        except (ThemeSettings.DoesNotExist, OperationalError):
            return 'core/theme/fast_theme/views'
    return 'core/theme/fast_theme/views'

def get_debug():
    if apps.ready:
        try:
            from setup.models import BaseSettings
            setup = BaseSettings.objects.get()
            DEBUG = setup.debugging_mode
        except (BaseSettings.DoesNotExist, OperationalError):
            DEBUG = True
        return DEBUG
    return True
