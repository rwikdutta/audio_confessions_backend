from django.apps import AppConfig
#from django.utils.translation import ugettext_lazy as _

class LikesConfig(AppConfig):
    name='likes'
    verbose_name= ('likes')

    def ready(self):
        import likes.signals
