from django.db import models
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth

from .utils import Util

User = get_user_model()
from .models import Abonne


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')
        
    def create(self, validated_data):
        email_body = 'Hello  '+ validated_data['username'] + "\n\n Thank you for visiting our L-mobile marathon site https://marathon.l-mobile.com/ \n\n Best regards \nL-mobile-marathon \n"
        data = {'email_body': email_body, 'to_email': validated_data['email'],
                    'email_subject': 'Welcome to our site '}
        Util.send_email(data)
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)


    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens','id','is_superuser','username']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)
        print("user",user)
        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'is_superuser':user.is_superuser,
            'username ':user.username,
            'email': user.email,
            'tokens': user.tokens,
            'id': user.id
            
        }

        return super().validate(attrs)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class ViewUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Abonne
        fields = ('id','email', 'username','is_admin','is_active','is_staff','is_superuser','date_de_naissance ','numero_de_tel','type')



class UpdateUserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True)
    
    class Meta:
        model = Abonne
        fields = ('id','email', 'username','is_admin','is_active','is_staff','is_superuser','date_de_naissance ','numero_de_tel','type')
        extra_kwargs = {
            'id': {'required': False},
            'email': {'required': False},
            'username': {'required': False},
            'is_admin': {'required': False},
            'is_active': {'required': False},
            'is_staff': {'required': False},
            'is_superuser': {'required': False},
            'date_de_naissance': {'required': False},
            'numero_de_tel': {'required': False},
            'type': {'required': False},
        }
        
  
    
    def update(self, instance, validated_data):

        instance.email = validated_data['email']
        instance.date_de_naissance = validated_data['date_de_naissance']
        instance.numero_de_tel = validated_data['numero_de_tel']
        instance.type = validated_data['type']
        instance.save()

        return instance
