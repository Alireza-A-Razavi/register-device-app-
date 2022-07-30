from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, get_user_model

from rest_framework import (
    permissions, 
    authentication, 
    views, 
    generics, 
    response, 
    status,
)

from .serializers import UserReplicaSerializer, UserSerializer

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