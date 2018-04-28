from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Likes
from bppimt_farewell_backend.constants import ALLOWED_MODELS_FOR_LIKE_AND_COMMENT
import logging

logger=logging.getLogger(__name__)

@receiver(post_save,sender=Likes,dispatch_uid='likes_post_save_uid')
def likes_post_save_handler(sender,instance,created,**kwargs):
    #logger.error("Inside likes_post_save_handler")
    if created and instance.content_type.model_class() in ALLOWED_MODELS_FOR_LIKE_AND_COMMENT:
        #logger.error("Inside if of likes_post_save_handler")
        instance.content_object.likes_count=instance.content_object.likes_count+1
        instance.content_object.save()


@receiver(post_delete,sender=Likes,dispatch_uid='likes_post_delete_uid')
def likes_post_delete_handler(sender,instance,**kwargs):
    #logger.error("Inside likes_post_delete_handler")
    if instance.content_type.model_class() in ALLOWED_MODELS_FOR_LIKE_AND_COMMENT:
        #logger.error("Inside if of likes_post_delete_handler")
        if instance.content_object is not None:
            instance.content_object.likes_count=instance.content_object.likes_count-1
            instance.content_object.save()






