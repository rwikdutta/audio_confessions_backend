import os
from django.contrib.contenttypes.models import ContentType

from authentication.permissions import AdminAccessPermission
from authentication.serializers import StudentModelSerializer
from hashtags.serializers import TagSerializer
from comment.serializers import CommentSerializer
from likes.models import Likes
from .models import Confessions
import datetime
from django.utils.timezone import utc
from django.contrib.auth.models import User
from authentication.models import StudentModel
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.core.exceptions import ObjectDoesNotExist
from bppimt_farewell_backend.constants import CONFESSION_FILE_EXTENSION,get_local_uploaded_files_path
from shutil import copyfile
import boto3
from django.core import exceptions
import librosa
import math

FILE_UPLOAD_DIR=get_local_uploaded_files_path()

class ConfessionsSerializer(serializers.HyperlinkedModelSerializer):
    #student = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='studentmodel-detail')
    student=serializers.SerializerMethodField(read_only=True)
    #username=serializers.CharField(source='student.user.username',read_only=True)
    username=serializers.SerializerMethodField(read_only=True)
    student_id=serializers.IntegerField(source='student.id',read_only=True)
    content_type_id=serializers.SerializerMethodField(read_only=True)
    object_id=serializers.IntegerField(source='id')
    comments_url=serializers.SerializerMethodField(read_only=True)
    can_delete=serializers.SerializerMethodField(read_only=True)
    self_like = serializers.SerializerMethodField(read_only=True)
    all_likes=serializers.SerializerMethodField(read_only=True)
    highlighted_comments=serializers.SerializerMethodField(read_only=True)
    #comments_count=serializers.SerializerMethodField(read_only=True)
    #likes_count=serializers.SerializerMethodField(read_only=True)
    tags=serializers.SerializerMethodField(read_only=True)
    student_obj=serializers.SerializerMethodField(read_only=True)

    def get_student_obj(self,obj):
        return StudentModelSerializer(instance=obj.student,context={'request':self.context['request']}).data

    def get_tags(self,obj):
        request = self.context['request']
        return TagSerializer(obj.tags.all(),context={'request': request},many=True).data

    # def get_likes_count(self,obj):
    #     return obj.likes.count()

    # def get_comments_count(self,obj):
    #     return obj.comments.count()

    def get_highlighted_comments(self,obj):
        request = self.context['request']
        comments=obj.comments.order_by('-id')[0:2]
        return CommentSerializer(comments,context={'request': request},many=True).data

    def get_all_likes(self,obj):
        request=self.context['request']
        return "{}?content_type__id={}&object_id={}".format(reverse('likesfilter', request=self.context['request']),obj.likes.content_type.id, obj.pk)

    def get_self_like(self,obj):
        request=self.context['request']
        student = StudentModel.objects.get(user=request.user)
        content_type_obj = ContentType.objects.get_for_model(obj)
        try:
            like=Likes.objects.get(student=student,content_type=content_type_obj,object_id=obj.id)
        except ObjectDoesNotExist:
            return None
        return reverse('likes-detail',args=(like.id,),request=request)

    def get_username(self,obj):
        if not obj.is_anonymous:
            return obj.student.user.username
        return None

    def get_can_delete(self,obj):
        request=self.context['request']
        # The below condition is for testing purposes when i sometimes disable IsAuthenticated check to test it from within the browser
        if not request.user.is_authenticated:
            return False
        if obj.student.user.id==request.user.id or AdminAccessPermission().has_permission(request=request,view=None):
            return True
        return False

    def get_student(self,obj):
        if not obj.is_anonymous:
            return reverse('studentmodel-detail',args=[obj.student.id],request=self.context['request'])
        return None

    def get_comments_url(self,obj):
        return "{}?content_type__id={}&object_pk={}".format(reverse('commentfilter',request=self.context['request']),obj.comments.content_type.id,obj.pk)

    def get_content_type_id(self,obj):
        return obj.comments.content_type.id

    class Meta:
        model = Confessions
        exclude = ('is_approved', 'modified_at')
        depth = 1
        # INFO: Since we dont have a view for user, we can't traverse deeper using HyperLinkedModelSerializer...as of now, I feel the only extra user info that the front end might require is user name, so i am including it as a seperate field here...


class AddConfessionsSerializer(serializers.Serializer):
    """
        Returns a Confessions model object
    """

    student_id=serializers.IntegerField(allow_null=False)
    datafile=serializers.FileField()
    description=serializers.CharField(max_length=256,allow_null=True,allow_blank=True)
    is_anonymous=serializers.BooleanField(default=False)
    tags=serializers.CharField(max_length=2048,allow_null=True,allow_blank=True)

    def validate(self, attrs):
        try:
            StudentModel.objects.get(id=attrs['student_id'])
        except ObjectDoesNotExist:
            raise exceptions.ValidationError({"student_id":"Student object doesnt exist"})
        return attrs

    #TODO: Add checking for content-types....Need to discuss this with the front-end developers

    def upload_file_to_s3(self,datafile,student_id):
        aws_region = 'ap-south-1'
        aws_folder = 'v1'
        s3_bucket_name='bpp-user-files'
        #s3_bucket_name=aws_bucket
        #aws_access_key=os.environ.get('SIH_S3_ACCESS_KEY')
        #aws_secret_key=os.environ.get('SIH_S3_SECRET_ACCESS_KEY')
        #TODO: Make aws_region an environment variable
        #TODO: Understand how the permissions are being set up since aws_access_key and aws_secret_key are not being used here...because aws-cli is already set up
        uploaded_at=datetime.datetime.utcnow().replace(tzinfo=utc)
        s3=boto3.resource('s3')
        file_name="{}_{}_{}{}".format('conf',student_id,uploaded_at.strftime('%Y%m%d%H%M%S'),CONFESSION_FILE_EXTENSION)
        temp_file_path=datafile.temporary_file_path()
        new_file_path=FILE_UPLOAD_DIR+file_name
        copyfile(temp_file_path,new_file_path)
        #TODO: Make proper naming conventions for file upload...make sure that whatever name you allow doesnt adversely affect any of the sql queries i.e. the values that you choose doesnt have any special meaning in sql query
        s3_file_name="{}/{}".format(aws_folder,file_name)
        resp=s3.Object(s3_bucket_name,s3_file_name).put(Body=open(new_file_path,'rb'), ACL='public-read')
        if resp['ResponseMetadata']['HTTPStatusCode']==200:
            return {'uploaded':True,'file_url':r"https://s3.{}.amazonaws.com/{}/{}/{}".format(aws_region,s3_bucket_name,aws_folder,file_name),'file_name':file_name,'uploaded_at':uploaded_at,'file_size':datafile.size,'new_file_path':new_file_path,'file_type':CONFESSION_FILE_EXTENSION}
        else:
            return {'uploaded':False}

    def create(self, validated_data):
        datafile=validated_data['datafile']
        resp=self.upload_file_to_s3(datafile,validated_data['student_id'])
        if resp['uploaded']==False:
            raise exceptions.ValidationError({'confession_clip_url':'Failed To Save Confession Clip...Try Again'})
        y, sr = librosa.load(resp['new_file_path'])
        confession_clip_duration=librosa.get_duration(y=y,sr=sr)
        confession=Confessions.objects.create(student_id=validated_data['student_id'],description=validated_data['description'],confession_clip_url=resp['file_url'],confession_clip_size=resp['file_size'],confession_clip_duration=math.ceil(confession_clip_duration),is_anonymous=validated_data['is_anonymous'])
        tags_arr=validated_data['tags'].lower().split(',')
        confession.tags.add(*tags_arr)
        return confession
