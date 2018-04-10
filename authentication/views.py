from django.shortcuts import render
from rest_framework.views import APIView,status
from django.core.exceptions import ObjectDoesNotExist

from authentication.models import StudentModel
from authentication.serializers import SignUpSerializer,SignInSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class SignUp(APIView):
    """
    Request Type: POST
    It allows you to sign up after sending the following details:

    Request Parameters:
        name,year,passout_year,dept,username,password,email

    Response Parameters (Incase of no errors):
        error=False
        token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        message=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    Response Parameters (Incase of errors):
        error=True
        message=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        error_fields=<describes parameter wise, the errors obtained>
    """

    def post(self,request):
        data_dict=request.data.dict()
        serializer=SignUpSerializer(data=data_dict)
        if serializer.is_valid():
            obj=serializer.save()
            token=Token.objects.create(user=obj.user)
            return Response({'error':False,'message':'User created successfully!','token':token.key,'username':data_dict['username']})
        else:
            return Response({'error':True,'error_fields':serializer.errors,'message':'Error Occured!'},status=status.HTTP_400_BAD_REQUEST)

class SignIn(APIView):
    """
        Request Type: POST
        It allows you to sign in after sending the following details:

        Request Parameters:
            username,password

        Response Parameters (Incase of no errors):
            error=False
            token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            message=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        Response Parameters (Incase of errors):
            error=True
            message=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            error_fields=<describes parameter wise, the errors obtained>
        """
    def post(self,request):
        data=request.data.dict()
        serializer=SignInSerializer(data=data)
        if serializer.is_valid():
            user=serializer.save()
            try:
                token=Token.objects.get(user=user)
            except ObjectDoesNotExist:
                token=Token.objects.create(user=user)
            return Response({'error':False,'message':'Signed In Successfully','token':token.key})
        else:
            return Response({'error':True,'message':'Error Occured','error_fields':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class SignOut(APIView):
    """
    Request Type: GET
    It allows you to sign out. The existing token will be invalidated and a new token will be generated the next time you sign in. Do note that signing out will sign the user out from all devices

    Request:
    Header: <Should contain authorization token, otherwise 401 error>

    Parameters: <None>

    Response:
    Error=True/False
    Message=xxxxxxxxxxxxxxxxxxxxx
    """
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        user=request.user
        token=Token.objects.get(user=user)
        token.delete()
        return Response({'error':False,'message':'Logged out successfully!'})

class CheckLogin(APIView):
    """
        Request Type: GET
        Allows you to check whether a token is still valid. Should be done at the time of the app being opened

        Request:
        Header: <Should contain authorization token>

        Parameters: <None>

        Response:
        Error=True/False
        isAuthenticated=True/False
        Message=xxxxxxxxxxxxxxxxxxxxx
        """

    def get(self,request):
        if request.user.is_authenticated:
            return Response({'error':False,'isAuthenticated':True,'message':'Logged in as {}'.format(request.user.username),'username':request.user.username})
        else:
            return Response({'error': False,'isAuthenticated':False, 'message': 'Not Logged In'})

class CheckAdminLogin(APIView):
    """
        Request Type: GET
        Allows you to check whether the logged in user is an admin or not. Should be done at the time of the app being opened, after the check for login

        Request:
        Header: <Should contain proper authorization token, otherwise 401 error>

        Parameters: <None>

        Response:
        Error=True/False
        isAdmin=True/False
        Message=xxxxxxxxxxxxxxxxx
    """
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        if request.user.is_authenticated:
            student = StudentModel.objects.get(user=request.user)
            if student.is_admin:
                return Response({'error':False,'isAdmin':True,'message':'Admin Privileges Enabled','username':request.user.username})
        return Response({'error':False,'isAdmin':False,'message':'User Privileges Enabled','username':request.user.username})