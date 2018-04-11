from django_comments.models import Comment
from authentication.models import StudentModel
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.reverse import reverse

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='comment-detail')
    student_url=serializers.SerializerMethodField()
    #TODO: Add a similar url for content-type after ensuring that all the content types have their corresponding views

    def get_student_url(self,obj):
        student=StudentModel.objects.get(user=obj.user)
        return reverse('studentmodel-detail',args=[student.id],request=self.context['request'])

    class Meta:
        model=Comment
        fields=('url','object_pk','user_name','user_email','user_url','comment','submit_date','ip_address','student_url')


