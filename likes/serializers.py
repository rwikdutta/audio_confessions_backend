from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from .models import Likes
from rest_framework.reverse import reverse
from rest_framework import serializers

class LikesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=Likes
        fields=('url','object_id','content_type_id','student')
        #exclude=('created_at',)
        #fields='__all__'

class AddLikesSerializer(serializers.Serializer):
    content_type_id=serializers.IntegerField(allow_null=False)
    object_id=serializers.IntegerField(allow_null=False)
    student_id=serializers.IntegerField(allow_null=False)

    def validate(self, attrs):
        try:
            ct_obj = ContentType.objects.get_for_id(attrs['content_type_id'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"content_type_id": "Invalid Content Type"})
        ct_obj_model = ct_obj.model_class()
        try:
            ct_obj_model.objects.get(id=attrs['object_id'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"object_id": "Object Does Not Exist"})
        try:
            Likes.objects.get(student=attrs['student_id'],content_type_id=attrs['content_type_id'],object_id=attrs['object_id'])
        except ObjectDoesNotExist:
            return attrs
        raise serializers.ValidationError({'student_id':'Like already exists'})

    def create(self, validated_data):
        return Likes.objects.create(**validated_data)