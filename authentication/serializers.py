from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core import exceptions
from rest_framework.authtoken.models import Token
from .models import StudentModel
import  django.contrib.auth.password_validation as validators

class SignUpSerializer(serializers.Serializer):

    name=serializers.CharField(max_length=256,allow_null=False)
    year=serializers.DecimalField(max_digits=1,decimal_places=0,allow_null=False)
    dept=serializers.CharField(max_length=3,allow_null=False)
    passout_year=serializers.DecimalField(max_digits=4,decimal_places=0,allow_null=False)
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
        if attrs['dept']=='MCA' and (attrs['year']<1 or attrs['year']>2):
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



