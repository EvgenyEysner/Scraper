from django.apps import AppConfig


class CianConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cian'

    verbose_name = 'Панель администратора'

    # override the method ready,
    # so that when our application is ready, a module with all handler functions is imported
    def ready(self):
        import cian.signals
