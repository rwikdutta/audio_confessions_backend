from django.db.models import F
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser

from authentication.models import StudentModel
from likes.models import Likes
from likes.serializers import LikesSerializer
from .models import Confessions
from .serializers import ConfessionsSerializer,AddConfessionsSerializer
from rest_framework import viewsets, mixins, views, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class ConfessionsViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise serializers.ValidationError({'error': True, 'message': 'Not Authenticated'})
        try:
            student_id_of_confession=Confessions.objects.get(pk=kwargs['pk']).student.user.id
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'error':True,'message':'Deleted Object Does Not Exist'})
        if request.user.id==student_id_of_confession:
            return super().destroy(request, *args, **kwargs)
        else:
            raise serializers.ValidationError({'error':True,'message':'No Delete Permission'})

    queryset = Confessions.objects.filter(is_approved=True).order_by('-id')
    serializer_class = ConfessionsSerializer
    permission_classes = (IsAuthenticated,)


class AddConfessionView(views.APIView):
    """
            Endpoint to Add a Confession

            Header=<Needs authentication token>

            Parameters:
                datafile=<Audio clip>
                description=xxxxxxxxx
                is_anonymous=True/False
        """
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsAuthenticated,)


    def post(self,request):
        request_data=request.data.dict()
        request_data['student_id']=StudentModel.objects.get(user=request.user).id
        serializer=AddConfessionsSerializer(data=request_data,context=request)
        if serializer.is_valid(raise_exception=False):
            confession=serializer.save()
            read_serializer=ConfessionsSerializer(confession,context={'request':request})
            return Response({'error':False,'message':'Confession was added successfully!','object':read_serializer.data})
        else:
            return Response({'error':True,'message':'Error Occured','error_fields':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class ConfessionStudentFilterView(generics.ListAPIView):
    queryset = Confessions.objects.filter(is_anonymous=False).order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('student__id',)
    serializer_class = ConfessionsSerializer
    permission_classes = (IsAuthenticated,)

class OrderedConfessionsViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Confessions.objects.filter(is_approved=True).order_by((F('likes_count')+F('comments_count')).desc(),'-id')
    serializer_class = ConfessionsSerializer
    permission_classes = (IsAuthenticated,)


