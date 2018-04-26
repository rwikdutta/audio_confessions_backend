from django.apps import AppConfig
#from django.utils.translation import ugettext_lazy as _

class CommentConfig(AppConfig):
    name='comment'
    verbose_name= ('comment')

    def ready(self):
        import comment.signals
