from taggit.models import Tag
from confessions.models import Confessions
from rest_framework.serializers import HyperlinkedModelSerializer,SerializerMethodField
#from rest_framework import serializers


class TagSerializer(HyperlinkedModelSerializer):
#TODO: Add extra fields for the discover page in a different serializer ( perhaps create a seperate app for that to prevent circular dependency and then add a reverse-link to this so that it can still be linked )
    class Meta:
        model=Tag
        exclude=('slug',)
