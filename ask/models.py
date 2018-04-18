from django.db import models
from authentication.models import StudentModel
from django.contrib.contenttypes.fields import GenericRelation
from django_comments.models import Comment
from likes.models import Likes
from taggit.managers import TaggableManager

# Create your models here.

class Ask(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    from_student=models.ForeignKey(StudentModel,on_delete=models.CASCADE,related_name='ask_from_student')
    question=models.CharField(max_length=3000,null=False)
    answer=models.CharField(max_length=3000,null=True,blank=True)
    answered_at=models.DateTimeField(null=True,blank=True)
    is_anonymous=models.BooleanField(default=False)
    to_student=models.ForeignKey(StudentModel,on_delete=models.CASCADE,related_name='ask_to_student')
    comments = GenericRelation(Comment, related_query_name='asks', related_name='asks',object_id_field='object_pk')
    likes = GenericRelation(Likes, related_name='asks', related_query_name='asks', object_id_field='object_id')
    tags = TaggableManager()

    def __str__(self):
        return "Q from {}:{} , A by {}:{}".format(self.from_student.user.username,self.question,self.to_student.user.username,self.answer)


