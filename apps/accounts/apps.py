from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'User Accounts'

    def ready(self):
        # Connect the post_save signal so every new User auto-gets a Profile
        from . import signals  # noqa: F401
