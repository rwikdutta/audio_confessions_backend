from django.db import models
from authentication.models import StudentModel
from django.contrib.contenttypes.fields import GenericRelation
from django_comments.models import Comment


# Create your models here.

class Confessions(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    student=models.ForeignKey(StudentModel,on_delete=models.DO_NOTHING,null=False)
    confession_clip_url=models.URLField(max_length=256,null=False)
    description=models.CharField(max_length=256,null=True,blank=True)
    is_approved=models.BooleanField(default=True)
    is_anonymous=models.BooleanField(default=False)
    confession_clip_size=models.IntegerField(null=False)
    confession_clip_duration=models.IntegerField(null=False)
    comments=GenericRelation(Comment,related_query_name='confessions',related_name='confessions',object_id_field='object_pk')

    def __str__(self):
        return "{}:{}".format(self.student.user.username,self.description)
