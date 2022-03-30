
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
    def ready(self):
            print("at ready")
            import user.signals
            # post_save.connect(create_user_profile, sender=User)
            # post_save.connect(save_user_profile, sender=User)
