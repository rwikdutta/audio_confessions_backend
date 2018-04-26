from django.db import models
from taggit.models import Tag
# Create your models here.

class TagCount(models.Model):
    tag=models.OneToOneField(to=Tag,primary_key=True,on_delete=models.CASCADE)
    count=models.IntegerField(default=0)

    class Meta:
        ordering=['-count','-tag_id']
