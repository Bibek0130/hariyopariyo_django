from django.apps import AppConfig

#defining a custom AppConfig class
class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

#using the get_app_config() method to retrieve the AppConfig instance for app
# store_app_config = apps.get_app_config('store')
