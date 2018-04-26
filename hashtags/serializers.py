from taggit.models import Tag
from confessions.models import Confessions
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.reverse import reverse
from rest_framework import serializers


class TagSerializer(HyperlinkedModelSerializer):
#TODO: Add extra fields for the discover page in a different serializer ( perhaps create a seperate app for that to prevent circular dependency and then add a reverse-link to this so that it can still be linked )
    confessions=serializers.SerializerMethodField(read_only=True)
    ask=serializers.SerializerMethodField(read_only=True)

    def get_confessions(self,obj):
        request=self.context['request']
        return "{}?tags__name__in={}".format(reverse('tagconfessionfilter', request=self.context['request']),obj.name)

    def get_ask(self,obj):
        request=self.context['request']
        return "{}?tags__name__in={}".format(reverse('tagaskfilter', request=self.context['request']),obj.name)

    class Meta:
        model=Tag
        exclude=('slug',)

class OrderedTagSerializer(TagSerializer):
    count=serializers.IntegerField(source='tagcount.count')

    class Meta:
        model=Tag
        exclude=('slug',)

