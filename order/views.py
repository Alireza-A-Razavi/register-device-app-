from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, response, authentication, status

User = get_user_model()

from .models import PaidOrder, DeviceToken
from .serializers import DeviceTokenModelSerializer, OrderModelSerializer, VerifyDeviceTokenSerializer
from .utils import try_password
from .permissions import DevicePermission

class ReplicaOrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderModelSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]
    queryset = PaidOrder.objects.all()


class DeviceTokenCreateAPIView(generics.CreateAPIView):
    serializer_class = DeviceTokenModelSerializer
    authentication_classes = [authentication.TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated, DevicePermission]
    queryset = DeviceToken.objects.all()


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


# ==============================================================
#
#                 Dajngo Views
#
# ==============================================================
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

class ValidateAndRegsiterUserView(View):

    def get(self, request):
        return render(request, "validate-register-user.html", context={})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        wp_validation_code, _cred_ok = try_password(
            "https://algotik.ir/xmlrpc.php",
            username, password
        )
        if _cred_ok:
            if password and username:
                try:
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                    messages.success(request, "success")
                    return redirect("/register-product/success/")
                except User.DoesNotExist:
                    try:
                        user = User.objects.get(phone_number=username)
                        user.set_password(password)
                        user.save()
                        messages.success(request, "success")
                        return redirect("/register-product/success/")
                    except User.DoesNotExist:
                        messages.warning(request, "کاربری با این نام کاربری وجود ندارد")
                        return redirect('/register-product/')
            else:
                messages.warning(request, "شماره تلفن یا گذرواژه شما اشتباه است.")
                return redirect("/register-product/")
        else:
            messages.warning(request, "شماره تلفن یا گذرواژه شما اشتباه است.")
            return redirect("/register-product/")


class SuccessProduct(View):
    
    def get(self, request):
        return render(request, "product-success.html")