from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer,AddCommentSerializer
from django_comments.models import Comment
from rest_framework import views, viewsets, mixins, permissions, generics, status
from django_filters.rest_framework import DjangoFilterBackend
import boto3
import datetime
from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import utc
from rest_framework.parsers import MultiPartParser,FormParser

# Create your views here.

#TODO: Remove ListModelMixin from CommentView since it doesn't seem fair that all of the comments can be accessed by anyone at one single go...
class CommentView(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):

    queryset = Comment.objects.filter(is_public=True,is_removed=False)
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise ValidationError({'error': True, 'message': 'Not Authenticated'})
        try:
            user_id_of_obj=Comment.objects.get(id=kwargs['pk']).user.id
        except ObjectDoesNotExist:
            raise ValidationError({'error':True,'message':'Comment doesnt exist'})
        if not user_id_of_obj==request.user.id:
            raise ValidationError({'error': True, 'message': 'No Delete Permission'})
        return super().destroy(request, *args, **kwargs)

class CommentFilterView(generics.ListAPIView):
    queryset = Comment.objects.filter(is_public=True,is_removed=False)
    filter_backends = (DjangoFilterBackend,)
    filter_fields=('content_type__id','object_pk')
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)


class AddCommentView(views.APIView):
    permission_classes = (IsAuthenticated,)
    """

        Endpoint to Add a Confession

        Header=<Needs authentication token>

        Parameters:
            comment=xxxxxxxxxxxx
            content_type_id=xx
            object_pk=xx
    """

    #TODO: Add checks to ensure that only the allowable models have comments attached to them ( once the full application is built)
    def post(self,request):
        request_data=request.data.dict()
        request_data['user_id']=request.user.id
        serializer=AddCommentSerializer(data=request_data)
        if serializer.is_valid(raise_exception=False):
            comment_obj=serializer.save()
            read_serializer=CommentSerializer(comment_obj,context={'request':request})
            return Response({'error':False,'message':'Comment Added Successfully','object':read_serializer.data})
        else:
            return Response({'error':True,'message':'Error Occurred','error_fields':serializer.errors},status=status.HTTP_400_BAD_REQUEST)





