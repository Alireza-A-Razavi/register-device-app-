from wsgiref.util import request_uri
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, get_user_model
from pkg_resources import require

from rest_framework import (
    permissions, 
    authentication, 
    views, 
    generics, 
    response, 
    status,
)

from .serializers import UserReplicaSerializer, UserSerializer, UserDetailSerializer
from .utils import user_verify_and_creation

User = get_user_model()

def get_async_csrf_token(request):
    csrftoken = get_token(request)
    return JsonResponse({'csrftoken':csrftoken})

class ReplicaUserCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    authentication_classes = []
    serializer_class = UserReplicaSerializer
    queryset = User.objects.all()

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        try:
            password = request.data.get("password")
            username = request.data.get("username")
            if password and username:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    message = "Successfully logined"
                    status_code = status.HTTP_200_OK
                else:
                    message = "Wrong password or username"
                    status_code = status.HTTP_200_OK
            else:
                message =  "Provide username and password!"
                status_code = status.HTTP_400_BAD_REQUEST
        except KeyError:
            message =  "Provide username and password!"
            status_code = status.HTTP_400_BAD_REQUEST
        
        return response.Response(
            {"message": message},
            status=status_code
        )


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status


class CustomAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        data = user_verify_and_creation(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        user = data.get("user")
        status_code = data.get("status_code")
        if user:
            serializer = self.serializer_class(data=request.data,
                                                context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return response.Response(data = {
                'token': token.key,
                'user_id': user.pk,
                'wp_user_id': user.wp_user_id,
                "user": UserDetailSerializer(user).data,
                "msg": "You have successfully logged in." 
            }, status=status_code)
        else:
            return response.Response({
                'token': None,
                'user_id': None,
                'wp_user_id': None,
                "msg": "Wrong credentials.",
            }, status=status_code)

class SimpleLoginAPIView(ObtainAuthToken):

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                                context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return response.Response(data = {
                'token': token.key,
                'user_id': user.pk,
                "msg": "You have successfully logged in." 
            }, status=status.HTTP_200_OK)
