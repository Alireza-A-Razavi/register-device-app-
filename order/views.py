from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, response, authentication, status

User = get_user_model()

from .utils import perform_raise_permission
from .models import PaidOrder, DeviceToken
from .serializers import (
    DeviceTokenModelSerializer, 
    OrderModelSerializer, 
    VerifyDeviceTokenSerializer, 
    DeviceAddPluginSerialzier,
)
class ReplicaOrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderModelSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]
    queryset = PaidOrder.objects.all()


class DeviceTokenCreateAPIView(generics.CreateAPIView):
    serializer_class = DeviceTokenModelSerializer
    authentication_classes = [authentication.TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated]
    queryset = DeviceToken.objects.all()


class DeviceTokenAddPlugin(generics.CreateAPIView):
    serializer_class = DeviceAddPluginSerialzier
    authentication_classes = [authentication.TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated,]


class DeviceTokenVerifyAPIView(generics.GenericAPIView):
    serializer_class = VerifyDeviceTokenSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,]
    queryset = DeviceToken.objects.all()

    def post(self, request, *args, **kargws):
        sered = self.serializer_class(data=request.data, context={"request": request})
        if sered.is_valid():
            return response.Response(
                {
                    "permission": sered.validate_the_token(validated_data=sered.validated_data), 
                    "success": True,
                }
            )
        else:
            return response.Response(
                {"permission": False, "success": True}
            )


class TestOptionsAPIView(generics.GenericAPIView):
    serializer_class = OrderModelSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        print(request.data)
        try:
            print(request.META)
        except Exception as E:
            print(E)
        return response.Response({"status": "OK"}, status=status.HTTP_200_OK)
    
    def get(self, request):
        print(request)
        return response.Response({"status": "OK"}, status=status.HTTP_200_OK)


class OrderUpdatePaymentStatusView(generics.GenericAPIView):
    serializer_class = OrderModelSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if request.data.get("status") == "paid":
            try:
                target_order = PaidOrder.objects.get(wp_order_id=request.data.get("id"))
                perform_raise_permission(target_order, customer_id=request.data.get("customer_id"))
                return response.Response(
                    data={"msg": "OK"},
                    status=status.HTTP_200_OK
                )
            except PaidOrder.DoesNotExist:
                print("The order has not been submitted")
                return response.Response(
                    data={"msg": "The order has not been added to the api"},
                    status=status.HTTP_400_BAD_REQUEST,
                )