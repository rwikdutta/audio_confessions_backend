from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from taggit.models import TaggedItem
from .models import TagCount
from django.core.exceptions import ObjectDoesNotExist
from bppimt_farewell_backend.constants import ALLOWED_MODELS_FOR_LIKE_AND_COMMENT
import logging

logger=logging.getLogger(__name__)

@receiver(post_save,sender=TaggedItem,dispatch_uid='tagged_item_post_save_uid')
def tagged_item_post_save_handler(sender,instance,created,**kwargs):
    #logger.error("Inside tagged_item_post_save_handler")
    if created and instance.content_type.model_class() in ALLOWED_MODELS_FOR_LIKE_AND_COMMENT:
        #logger.error("Inside if of tagged_item_post_save_handler")
        try:
            obj=TagCount.objects.get(tag_id=instance.tag_id)
        except ObjectDoesNotExist:
            obj=TagCount.objects.create(tag_id=instance.tag_id)
        obj.count=obj.count+1
        obj.save()


@receiver(post_delete,sender=TaggedItem,dispatch_uid='tagged_item_post_delete_uid')
def tagged_item_post_delete_handler(sender,instance,**kwargs):
    #logger.error("Inside tagged_item_post_delete_handler")
    if instance.content_type.model_class() in ALLOWED_MODELS_FOR_LIKE_AND_COMMENT:
        #logger.error("Inside if of tagged_item_post_delete_handler")
        try:
            obj=TagCount.objects.get(tag_id=instance.tag_id)
        except ObjectDoesNotExist:
            obj=TagCount.objects.create(tag_id=instance.tag_id)
        obj.count=obj.count-1
        obj.save()





