from django_comments.models import Comment
from authentication.models import StudentModel
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.reverse import reverse

from authentication.permissions import AdminAccessPermission
from authentication.serializers import StudentModelSerializer
from bppimt_farewell_backend.settings import SITE_ID
from likes.models import Likes


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    student_url = serializers.SerializerMethodField(read_only=True)
    can_delete = serializers.SerializerMethodField(read_only=True)
    username=serializers.CharField(source='user.username',read_only=True)
    student_obj=serializers.SerializerMethodField(read_only=True)
    # TODO: Add a similar url for content-type after ensuring that all the content types have their corresponding views

    def get_student_obj(self,obj):
        request = self.context['request']
        return StudentModelSerializer(instance=StudentModel.objects.get(user=obj.user),context={'request':request}).data

    def get_can_delete(self, obj):
        request = self.context['request']
        # The below condition is for testing purposes when i sometimes disable IsAuthenticated check to test it from within the browser
        if not request.user.is_authenticated:
            return False
        if obj.user.id == request.user.id or AdminAccessPermission().has_permission(request=request,view=None):
            return True
        return False

    def get_student_url(self, obj):
        student = StudentModel.objects.get(user=obj.user)
        return reverse('studentmodel-detail', args=[student.id], request=self.context['request'])


    class Meta:
        model = Comment
        fields = ('url', 'object_pk','comment', 'submit_date','student_url', 'can_delete', 'content_type_id','username','student_obj')


class AddCommentSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(allow_null=False)
    comment = serializers.CharField(max_length=3000, allow_null=False)
    object_pk = serializers.IntegerField(allow_null=False)
    content_type_id = serializers.IntegerField(allow_null=False)

    def validate(self, attrs):
        try:
            ct_obj = ContentType.objects.get_for_id(attrs['content_type_id'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"content_type_id": "Invalid Content Type"})
        ct_obj_model = ct_obj.model_class()
        try:
            ct_obj_model.objects.get(id=attrs['object_pk'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"object_pk": "Object Does Not Exist"})
        return attrs

    def create(self, validated_data):
        return Comment.objects.create(**validated_data, is_public=True, is_removed=False, site_id=SITE_ID)
