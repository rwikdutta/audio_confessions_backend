from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer
from django_comments.models import Comment
from rest_framework import views,viewsets,mixins,permissions,generics
from django_filters.rest_framework import DjangoFilterBackend
import boto3
import datetime
from django.utils.timezone import utc
from rest_framework.parsers import MultiPartParser,FormParser


# Create your views here.

#TODO: Remove ListModelMixin from CommentView since it doesn't seem fair that all of the comments can be accessed by anyone at one single go...
#TODO: Custom define the method for DestroyModelMixin since there needs to be a permission check
class CommentView(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    queryset = Comment.objects.filter(is_public=True,is_removed=False)
    #TODO: Remove the comment from the permission_class
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

class CommentFilterView(generics.ListAPIView):
    queryset = Comment.objects.filter(is_public=True,is_removed=False)
    filter_backends = (DjangoFilterBackend,)
    filter_fields=('content_type__id','object_pk')
    serializer_class = CommentSerializer


#TODO: Generate a seperate view for creating  comments since in Comments, we are dealing with User and not Student directly in the model

class AddConfessionView(views.APIView):

    def post(self,request):
        request_data=request.data.dict()



