from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from authentication.permissions import AdminAccessPermission
from authentication.serializers import StudentModelSerializer
from comment.serializers import CommentSerializer
from hashtags.serializers import TagSerializer
from likes.models import Likes
from authentication.models import StudentModel
from .models import Ask
from rest_framework.reverse import reverse
import datetime
from django.utils.timezone import utc

class AskSerializer(serializers.HyperlinkedModelSerializer):
    to_student_obj=serializers.SerializerMethodField(read_only=True)
    from_student_obj = serializers.SerializerMethodField(read_only=True)
    to_student_username=serializers.CharField(source='to_student.user.username')
    content_type_id=serializers.SerializerMethodField(read_only=True)
    object_id=serializers.IntegerField(source='id')
    from_student=serializers.SerializerMethodField(read_only=True) #Because we might have to mask the value based on the value of is_anonymous
    from_student_username = serializers.SerializerMethodField(read_only=True) #Because we might have to mask the value based on the value of is_anonymous
    can_delete=serializers.SerializerMethodField(read_only=True)
    self_like=serializers.SerializerMethodField(read_only=True)
    all_likes=serializers.SerializerMethodField(read_only=True)
    highlighted_comments=serializers.SerializerMethodField(read_only=True)
    #likes_count=serializers.SerializerMethodField(read_only=True)
    #comments_count=serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    can_answer=serializers.SerializerMethodField(read_only=True)
    all_comments=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=Ask
        fields=('url','question','answer','is_anonymous','from_student','to_student','from_student_username','to_student_username','content_type_id','object_id','can_delete','self_like','all_likes','highlighted_comments','likes_count','tags','created_at','comments_count','can_answer','all_comments','answered_at','to_student_obj','from_student_obj')

    def get_to_student_obj(self,obj):
        request = self.context['request']
        return StudentModelSerializer(instance=obj.to_student,context={'request':request}).data

    def get_from_student_obj(self,obj):
        request = self.context['request']
        if obj.is_anonymous:
            return None
        return StudentModelSerializer(instance=obj.from_student, context={'request': request}).data

    def get_content_type_id(self,obj):
        return obj.comments.content_type.id

    def get_from_student(self,obj):
        request = self.context['request']
        if obj.is_anonymous:
            return None
        return reverse('studentmodel-detail',args=[obj.from_student.id],request=request)

    def get_from_student_username(self,obj):
        if obj.is_anonymous:
            return None
        return obj.from_student.user.username

    def get_can_delete(self,obj):
        request=self.context['request']
        if request.user.id==obj.from_student.user.id or AdminAccessPermission().has_permission(request=request,view=None):
            return True
        return False

    def get_self_like(self,obj):
        request = self.context['request']
        student = StudentModel.objects.get(user=request.user)
        content_type_obj = ContentType.objects.get_for_model(obj)
        try:
            like = Likes.objects.get(student=student, content_type=content_type_obj, object_id=obj.id)
        except ObjectDoesNotExist:
            return None
        return reverse('likes-detail', args=(like.id,), request=request)

    def get_all_likes(self,obj):
        request = self.context['request']
        return "{}?content_type__id={}&object_id={}".format(reverse('likesfilter', request=self.context['request']),obj.likes.content_type.id, obj.pk)

    def get_highlighted_comments(self,obj):
        request = self.context['request']
        comments = obj.comments.order_by('-id')[0:2]
        return CommentSerializer(comments, context={'request': request}, many=True).data

    # def get_likes_count(self,obj):
    #     return obj.likes.count()

    # def get_comments_count(self,obj):
    #     return obj.comments.count()

    def get_tags(self,obj):
        request = self.context['request']
        return TagSerializer(obj.tags.all(),context={'request': request},many=True).data

    def get_can_answer(self,obj):
        request=self.context['request']
        if request.user.id==obj.to_student.user.id:
            return True
        return False

    def get_all_comments(self,obj):
        request=self.context['request']
        return "{}?content_type__id={}&object_pk={}".format(reverse('commentfilter', request=self.context['request']),obj.comments.content_type.id, obj.pk)

class AnswerAskSerializer(serializers.Serializer):
    object_id=serializers.IntegerField(allow_null=False)
    answer=serializers.CharField(max_length=3000,allow_null=False,allow_blank=False)

    def validate(self, attrs):
        request=self.context['request']
        try:
            ask_obj=Ask.objects.get(id=attrs['object_id'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'object_id':'Invalid Object ID'})
        if ask_obj.to_student.user.id==request.user.id:
            return attrs
        raise serializers.ValidationError({'answer':'You Dont Have Permission To Answer'})

    def create(self, validated_data):
        ask_obj=Ask.objects.get(id=validated_data['object_id'])
        ask_obj.answer=validated_data['answer']
        ask_obj.answered_at=datetime.datetime.utcnow().replace(tzinfo=utc)
        ask_obj.save()
        return ask_obj

class AddAskSerializer(serializers.Serializer):
    question=serializers.CharField(max_length=3000,allow_blank=False,allow_null=False)
    is_anonymous=serializers.BooleanField(default=False)
    to_student_id=serializers.IntegerField(allow_null=False)
    tags=serializers.CharField(max_length=3000,allow_null=True,allow_blank=True)

    def validate(self, attrs):
        request=self.context['request']
        if attrs['to_student_id'] == StudentModel.objects.get(user=request.user).id:
            raise serializers.ValidationError({'to_student_id': 'You cannot ask a question to yourself'})
        try:
            to_student=StudentModel.objects.get(id=attrs['to_student_id'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'to_student_id':'Invalid Student ID'})
        return attrs

    def create(self, validated_data):
        request=self.context['request']
        from_student=StudentModel.objects.get(user=request.user)
        tags=validated_data['tags']
        tags_arr=tags.lower().split(',')
        tags_arr=[ar for ar in tags_arr if ar != '']
        obj=Ask.objects.create(question=validated_data['question'],is_anonymous=validated_data['is_anonymous'],from_student=from_student,to_student_id=validated_data['to_student_id'])
        obj.tags.add(*tags_arr)
        return obj








    
