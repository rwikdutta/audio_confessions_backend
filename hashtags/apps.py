from django.apps import AppConfig


class HashtagsConfig(AppConfig):
    name = 'hashtags'
    verbose_name=('hashtags')

    def ready(self):
        import hashtags.signals
