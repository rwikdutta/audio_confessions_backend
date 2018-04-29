import datetime
from shutil import copyfile
from PIL import Image
from resizeimage import resizeimage
import boto3
from django.utils.timezone import utc
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core import exceptions
from rest_framework.authtoken.models import Token
from bppimt_farewell_backend.constants import get_local_uploaded_files_path,ACCEPTED_PROFILE_PICTURE_TYPES
from .models import StudentModel
import  django.contrib.auth.password_validation as validators


class SignUpSerializer(serializers.Serializer):

    name=serializers.CharField(max_length=256,allow_null=False)
    year=serializers.DecimalField(max_digits=1,decimal_places=0,allow_null=False)
    dept=serializers.CharField(max_length=3,allow_null=False)
    passout_year=serializers.DecimalField(max_digits=4,decimal_places=0,allow_null=True,default=2019) #temp_hack
    username=serializers.CharField(max_length=128,allow_null=False)
    password=serializers.CharField(max_length=128,allow_null=False)
    email=serializers.EmailField(allow_null=False)


    def validate_dept(self,value):
        if value in {'CSE','ECE','IT','MCA','EE'}:
            return value
        else:
            raise serializers.ValidationError("Department Invalid")

    def validate_passout_year(self,value):
        if value in {2017,2018,2019,2020,2021,2022}:
            return value
        else:
            raise serializers.ValidationError("Passout Year Invalid")

    def validate_year(self,value):
        if value in {1,2,3,4}:
            return value
        else:
            raise serializers.ValidationError("Year Invalid")

    def validate_username(self,value):
        try:
            User.objects.get(username=value)
        except ObjectDoesNotExist:
            return value
        raise serializers.ValidationError("Username Exist")


    def validate_email(self,value):
        try:
            User.objects.get(email=value)
        except ObjectDoesNotExist:
            return value
        raise serializers.ValidationError("Email Exists")

    def validate(self, attrs):
        if attrs['dept']=='MCA' and (attrs['year']<1 or attrs['year']>3):
            raise serializers.ValidationError({"year":"Year Invalid For MCA"})

        user=User(attrs['username'],attrs['email'],attrs['password'])
        errors=dict()
        try:
            validators.validate_password(attrs['password'],user)
        except exceptions.ValidationError as e:
            errors['password']=list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return attrs




    def create(self, validated_data):
        user=User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
        fields_for_student=('name','year','dept','passout_year')
        data_dict=dict(validated_data)
        student_data_dict={k:v for k,v in data_dict.items() if k in fields_for_student}
        student=StudentModel.objects.create(user=user,**student_data_dict)
        return student

    #TODO: Not implemented yet in views
    def update(self, instance, validated_data):
        instance.year=validated_data.get('year',instance.year)
        instance.dept=validated_data.get('dept',instance.dept)
        instance.passout_year=validated_data.get('passout_year',instance.passout_year)
        instance.name=validated_data.get('name',instance.name)
        instance.user.email=validated_data.get('email',instance.user.email)
        instance.save()
        return instance

class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, allow_null=False)
    password = serializers.CharField(max_length=128, allow_null=False)


    def validate(self, attrs):
        try:
            user=User.objects.get(username=attrs['username'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"username":"Username Doesnt Exist"})
        if user.check_password(attrs['password']):
            return attrs
        raise serializers.ValidationError({"password":"Password Incorrect"})

    def create(self, validated_data):
        return User.objects.get(username=validated_data['username'])

class StudentModelSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='studentmodel-detail')
    username=serializers.CharField(source='user.username')
    user_confessions=serializers.SerializerMethodField(read_only=True)
    user_asks_from=serializers.SerializerMethodField(read_only=True)
    user_asks_to = serializers.SerializerMethodField(read_only=True)

    def get_user_asks_from(self,obj):
        return "{}?{}={}".format(reverse('fromstudentfilter', request=self.context['request']), 'from_student__id',obj.id)

    def get_user_asks_to(self, obj):
        return "{}?{}={}".format(reverse('tostudentfilter', request=self.context['request']), 'to_student__id',obj.id)

    def get_user_confessions(self,obj):
        return "{}?{}={}".format(reverse('confessionstudentfilter',request=self.context['request']),'student__id',obj.id)

    class Meta:
        model=StudentModel
        fields=('url','name','year','dept','passout_year','username','id','user_confessions','user_asks_from','user_asks_to','profile_picture_small_url','profile_picture_large_url',)

class UpdateProfilePictureSerializer(serializers.Serializer):
    profile_picture=serializers.FileField(allow_empty_file=False,allow_null=False)

    def validate_profile_picture(self,value):
        path=value.temporary_file_path()
        if path[path.rfind('.'):] in ACCEPTED_PROFILE_PICTURE_TYPES:
            return value
        raise serializers.ValidationError({'Accepted file types are .jpg,.jpeg and .png'})

    def upload_profile_picture_to_s3(self, file_path, student_id):
        FILE_UPLOAD_DIR = get_local_uploaded_files_path()
        aws_region = 'ap-south-1'
        aws_folder = 'v1'
        s3_bucket_name = 'bpp-user-files'
        # s3_bucket_name=aws_bucket
        # aws_access_key=os.environ.get('SIH_S3_ACCESS_KEY')
        # aws_secret_key=os.environ.get('SIH_S3_SECRET_ACCESS_KEY')
        # TODO: Make aws_region an environment variable
        # TODO: Understand how the permissions are being set up since aws_access_key and aws_secret_key are not being used here...because aws-cli is already set up
        uploaded_at = datetime.datetime.utcnow().replace(tzinfo=utc)
        s3 = boto3.resource('s3')
        temp_file_path = file_path
        extension = temp_file_path[temp_file_path.rfind('.'):]
        file_name = "{}_{}_{}{}".format('dp', student_id, uploaded_at.strftime('%Y%m%d%H%M%S'), extension)
        new_file_path = FILE_UPLOAD_DIR + file_name
        copyfile(temp_file_path, new_file_path)
        cover_name_512_512 = "{}_{}_512_{}{}".format('dp', student_id, uploaded_at.strftime('%Y%m%d%H%M%S'),extension)
        cover_name_96_96 = "{}_{}_96_{}{}".format('dp', student_id, uploaded_at.strftime('%Y%m%d%H%M%S'), extension)
        file_path_96 = FILE_UPLOAD_DIR + cover_name_96_96
        file_path_512 = FILE_UPLOAD_DIR + cover_name_512_512
        with open(new_file_path, 'r+b') as f:
            with Image.open(f) as image:
                if image.height < 512 or image.width < 512:
                    raise serializers.ValidationError({"profile_picture": "Images should be atleast 512*512"})
                cover = resizeimage.resize_cover(image, [512, 512])
                cover.save(file_path_512)
                cover_small = resizeimage.resize_cover(image, [96, 96])
                cover_small.save(file_path_96)
        # TODO: Make proper naming conventions for file upload...make sure that whatever name you allow doesnt adversely affect any of the sql queries i.e. the values that you choose doesnt have any special meaning in sql query
        s3_file_name_large = "{}/{}".format(aws_folder, cover_name_512_512)
        s3_file_name_small = "{}/{}".format(aws_folder, cover_name_96_96)
        resp_large = s3.Object(s3_bucket_name, s3_file_name_large).put(Body=open(file_path_512, 'rb'),ACL='public-read')
        if resp_large['ResponseMetadata']['HTTPStatusCode'] == 200:
            resp_small = s3.Object(s3_bucket_name, s3_file_name_small).put(Body=open(file_path_96, 'rb'),ACL='public-read')
            if resp_small['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {'uploaded': True,'file_url_large': r"https://s3.{}.amazonaws.com/{}/{}/{}".format(aws_region, s3_bucket_name,aws_folder, cover_name_512_512),'file_url_small': r"https://s3.{}.amazonaws.com/{}/{}/{}".format(aws_region, s3_bucket_name,aws_folder, cover_name_96_96),'file_type': extension}
        raise serializers.ValidationError({'profile_picture': 'Couldnt Update Profile Picture'})

    def create(self, validated_data):
        temp_path=validated_data['profile_picture'].temporary_file_path()
        request=self.context['request']
        student=StudentModel.objects.get(user=request.user)
        resp=self.upload_profile_picture_to_s3(temp_path,student.id)
        student.profile_picture_large_url=resp['file_url_large']
        student.profile_picture_small_url=resp['file_url_small']
        student.save()
        return student


