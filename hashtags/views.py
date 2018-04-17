from django.shortcuts import render
from rest_framework import viewsets,mixins
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TagSerializer
from taggit.models import Tag
# Create your views here.

class TagViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)


