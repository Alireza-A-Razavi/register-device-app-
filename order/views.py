from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, response, authentication

User = get_user_model()

from .models import PaidOrder, DeviceToken
from .serializers import DeviceTokenModelSerializer, OrderModelSerializer, VerifyDeviceTokenSerializer


class ReplicaOrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderModelSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]
    queryset = PaidOrder.objects.all()


class DeviceTokenCreateAPIView(generics.CreateAPIView):
    serializer_class = DeviceTokenModelSerializer
    authentication_classes = [authentication.SessionAuthentication,]
    permission_classes = [permissions.IsAuthenticated,]
    queryset = DeviceToken.objects.all()


class DeviceTokenVerifyAPIView(generics.GenericAPIView):
    serializer_class = VerifyDeviceTokenSerializer
    authentication_classes = [authentication.SessionAuthentication,]
    permission_classes = [permissions.IsAuthenticated,]
    queryset = DeviceToken.objects.all()

    def post(self, request, *args, **kargws):
        sered = self.serializer_class(request.data)
        if sered.is_valid():
            return response.Response(
                {"token": sered.token, "permission": sered.validate_token(), "success": True}
            )
        else:
            return response.Response(
                {"token": sered.token, "success": False}
            )