from django.apps import AppConfig
import traceback

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        try:
            import users.signals
            print("✅ DEBUG: users.signals imported successfully!")
        except Exception:
            print("❌ ERROR importing signals:")
            print(traceback.format_exc())


# from django.apps import AppConfig


# class UsersConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'users'

#     def ready(self):
#         import users.signals