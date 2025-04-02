from django.apps import AppConfig

class AppSetupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App_SetUp'

    def ready(self):
        try:
            import App_SetUp.signals
        except ImportError:
            pass

