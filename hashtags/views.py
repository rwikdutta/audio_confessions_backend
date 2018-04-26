from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ask.models import Ask
from ask.serializers import AskSerializer
from comment.serializers import CommentSerializer
from confessions.models import Confessions
from confessions.serializers import ConfessionsSerializer
from .serializers import TagSerializer,OrderedTagSerializer
from taggit.models import Tag
# Create your views here.

class TagViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

class OrderedTagViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Tag.objects.order_by('tagcount')
    serializer_class = OrderedTagSerializer
    permission_classes = (IsAuthenticated,)

class TagConfessionFilterView(generics.ListAPIView):
    serializer_class = ConfessionsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        tags__name__in=self.request.query_params.get('tags__name__in',None)
        if tags__name__in:
            return Confessions.objects.filter(tags__name__in=[tags__name__in],is_approved=True).distinct().order_by('-id')
        return Confessions.objects.order_by('-id')

class TagAskFilterView(generics.ListAPIView):
    serializer_class = AskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        tags__name__in = self.request.query_params.get('tags__name__in', None)
        if tags__name__in:
            return Ask.objects.filter(tags__name__in=[tags__name__in]).distinct().order_by('-id')
        return Ask.objects.order_by('-id')




