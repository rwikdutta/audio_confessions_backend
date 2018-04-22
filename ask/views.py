from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import mixins,viewsets,views,status,serializers,generics
from .models import Ask
from .serializers import AskSerializer,AnswerAskSerializer,AddAskSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.models import StudentModel
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class AskViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        try:
            ask_obj=Ask.objects.get(id=id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'error':True,'message':'Invalid Object'})
        if ask_obj.from_student.user.id==request.user.id:
            return super().destroy(request, *args, **kwargs)
        raise serializers.ValidationError({'error':True,'message':'No Permission to Delete'})

    queryset = Ask.objects.all()
    serializer_class = AskSerializer
    permission_classes = (IsAuthenticated,)

class AnswerAskView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        request_data=request.data.dict()
        serializer=AnswerAskSerializer(data=request_data,context={'request':request})
        if serializer.is_valid(raise_exception=False):
            obj=serializer.save()
            read_serializer=AskSerializer(obj,context={'request':request})
            return Response({'error':False,'message':'Ask Answered Successfully!','object':read_serializer.data})
        else:
            return Response({'error':True,'message':'Some Error Occured','error_fields':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class AddAskView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        request_data=request.data.dict()
        serializer=AddAskSerializer(data=request_data,context={'request':request})
        if serializer.is_valid(raise_exception=False):
            obj=serializer.save()
            read_serializer=AskSerializer(obj,context={'request':request})
            return Response({'error':False,'message':'Ask added successfully!','object':read_serializer.data})
        else:
            return Response({'error':True,'message':'Some error occured','error_fields':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class FromStudentAskFilterView(generics.ListAPIView):
    queryset = Ask.objects.filter(is_anonymous=False).order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('from_student__id',)
    serializer_class = AskSerializer
    permission_classes = (IsAuthenticated,)

class ToStudentAskFilterView(generics.ListAPIView):
    queryset = Ask.objects.order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('to_student__id',)
    serializer_class = AskSerializer
    permission_classes = (IsAuthenticated,)



