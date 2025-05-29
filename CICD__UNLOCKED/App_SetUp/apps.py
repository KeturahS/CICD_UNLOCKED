from django.apps import AppConfig

class AppSetupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App_SetUp'

    def ready(self):
        try:
            import App_SetUp.signals

            from App_SetUp.utils.load_scheduler import start_scheduler
            start_scheduler()

        except Exception as e:
            print(f"[Scheduler Error] {e}")
