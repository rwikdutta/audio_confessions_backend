from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.serializers import ValidationError
from rest_framework import viewsets, mixins, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.models import StudentModel
from .models import Likes
from .serializers import LikesSerializer,AddLikesSerializer
# Create your views here.

#TODO: Add checks to ensure that only the allowable models have likes attached to them ( once the full application is built)

class LikesViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):

    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise ValidationError({'error':True,'message':'Not Authenticated'})
        try:
            like=Likes.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            raise ValidationError({'error': True, 'message': 'Like Doesnt Exist'})
        if not like.student.id==StudentModel.objects.get(user=request.user).id:
            raise ValidationError({'error': True, 'message': 'Delete Like Not Permitted'})
        return super().destroy(request, *args, **kwargs)

class LikesFilterView(generics.ListAPIView):
    queryset = Likes.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields=('content_type__id','object_id')
    serializer_class = LikesSerializer
    permission_classes = (IsAuthenticated,)

class AddLikesView(APIView):
    """
    For adding a new like

    Authorization required

    Parameters:
        object_id=xxxx
        content_type_id=xxxx
    """
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        request_data=request.data.dict()
        request_data['student_id']=StudentModel.objects.get(user=request.user).id
        serializer=AddLikesSerializer(data=request_data)
        if serializer.is_valid(raise_exception=False):
            return Response({'error':False,'message':'Like Updated Successfully'})
        else:
            return Response({'error':True,'message':'Some Error Occurred While Updating Like','error_fields':serializer.errors},status=status.HTTP_400_BAD_REQUEST)