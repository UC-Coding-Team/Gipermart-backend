from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util


#  ************************    User Registration Serializer    ************************
class UserRegistrationSerilizer(serializers.ModelSerializer):
    # We are writing this bcoz we need confirm password field in our registration request
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)




#  ************************    User Login Serializer    ************************
class UserLoginSerilizer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']




#  ************************    User Profile Serializer    ************************
class UserProfileSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']




#  ************************    User Change Password Serializer    ************************
class UserChangePasswordSerilizer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)    
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)    
    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs



#  ************************    Send Password Reset Email Serializer    ************************
class SendPasswordResetEmailSerilizer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://www.127.0.0.1:3000/api/user/reset_password/'+uid+'/'+token
            print('Password Reset Link', link)
            # here email send code.
            data = {
                'subject':'Your Password Reset Link',
                'body':f"Click Following Link to Reset Your Password --->  {link}",
                'to_email':user.email
            }
            Util.send_email(data)

            return attrs
        else:
            raise serializers.ValidationError('You are not a Register User.')



#  ************************    User Password Reset Serializer    ************************
class UserPasswordResetViewSerilizer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)    
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)    
    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not valid or is expired!")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is not valid or is expired!")

