from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from authentication.models import StudentModel

# Create your models here.

class Likes(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    student=models.ForeignKey(StudentModel,on_delete=models.CASCADE)

    def __str__(self):
        return "{}:{}".format(self.content_type.name,self.object_id)

    class Meta:
        unique_together=(('content_type','object_id','student'),)