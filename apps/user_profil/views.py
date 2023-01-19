from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import UserRenderer, renderers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated



#  ************************    Tokken Genrated Class    ************************
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# Create your views here.
#  ************************    User Registraion View    ************************
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        get_tokens_for_user(user)
        return Response({"message":"registration success"}, status=status.HTTP_201_CREATED)



#  ************************    User Login View    ************************
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({"token":token,"message":"login success"}, status=status.HTTP_200_OK)
        else:
            return Response({"errors":{"non_field_errors":["Email or Password is not Valid"]}}, status=status.HTTP_401_UNAUTHORIZED)
        


#  ************************    User Profile View    ************************
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerilizer(request.user)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)



#  ************************    User Change Password View    ************************
class UserChangePassword(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerilizer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({"message":"your password successfully changed"}, status=status.HTTP_200_OK)



#  ************************    Send Password Reset Email View    ************************
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message":"Password reset link successfully send. Please check your email."}, status=status.HTTP_200_OK)



#  ************************    User Password Reset View    ************************
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetViewSerilizer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({"message":"your password successfully changed"}, status=status.HTTP_200_OK)
            


