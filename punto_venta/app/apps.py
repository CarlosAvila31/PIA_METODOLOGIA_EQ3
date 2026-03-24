from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    #el archivo signals.py para actualizar el total de venta
    def ready(self):
        import app.signals