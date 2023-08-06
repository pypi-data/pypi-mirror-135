from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_settings():
    DEFAULT_SETTINGS = {
        'queue_prefix': 'django-kiwi',
        'broker_url': None,
        'module_name': None,
    }

    ret = None
    settings_dict = {}

    try:
        ret = settings.DJANGO_KIWI
    except AttributeError:
        raise ImproperlyConfigured('DJANGO_KIWI settings is missing.')

    if type(ret) != dict:
        raise ImproperlyConfigured('DJANGO_KIWI setting must be a dict.')

    if 'broker_url' not in ret:
        raise ImproperlyConfigured('DJANGO_KIWI.broker_url is missing.')

    if 'module_name' not in ret:
        raise ImproperlyConfigured('DJANGO_KIWI.module_name is missing.')

    for key, value in DEFAULT_SETTINGS.items():
        settings_dict[key] = settings.DJANGO_KIWI.get(key, value)

    return dict(**settings_dict)
