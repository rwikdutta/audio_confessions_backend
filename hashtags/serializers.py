from taggit.models import Tag
from rest_framework.serializers import HyperlinkedModelSerializer

class TagSerializer(HyperlinkedModelSerializer):
#TODO: Add extra fields for the discover page later
    class Meta:
        model=Tag
        exclude=('slug',)