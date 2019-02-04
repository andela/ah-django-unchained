from django.apps import AppConfig


class FriendsConfig(AppConfig):
    name = 'authors.apps.friends'

    def ready(self):
        from authors.apps.usernotifications import handlers
