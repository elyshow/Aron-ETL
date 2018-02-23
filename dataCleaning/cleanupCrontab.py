from django_crontab.crontab import Crontab
from django_crontab.app_settings import Settings
from django.conf import settings as django_settings


class Crontab(Crontab):
    def __init__(self, **options):
        self.verbosity = int(options.get('verbosity', 1))
        self.readonly = options.get('readonly', False)
        self.crontab_lines = []
        if hasattr(options, 'settings'):
            self.settings = Settings(options['settings'])
        else:
            self.settings = Settings(django_settings)