from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from .serializers import CommentSerializer
from django_comments.models import Comment
from rest_framework import views,viewsets,mixins
from rest_framework import permissions


# Create your views here.

class CommentView(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    queryset = Comment.objects.filter(is_public=True)
    #aTODO: Remove the comment from the permission_class
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

