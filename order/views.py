from distutils.log import error
from itertools import product
from operator import ge
from urllib.request import Request
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseBadRequest


User = get_user_model()

from .models import Order, DeviceToken

class IndexView(View):

    def get(self, request):
        return render(request, "index.html", {})

class CreateOrderView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "create.html", context={})
        else:
            return Http404("not allowed")

    def post(self, request):
        if request.POST.get("name"):
            return redirect("/product")
        else:
            return HttpResponseBadRequest("You didn't provide the name")

class ProductPage(View):

    def get(self, request):
        return render(request, "product.html", context={})


from rest_framework import permissions, response, status, generics, authentication

from . serializers import OrderModelSerializer

class OrderCreateAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = OrderModelSerializer

    def post(self, request):
        print(request.META)
        if request.data.get("user"):
            user = User.objects.get(id=request.data.get("user"))
            orders = Order.objects.filter(user=user, device_token__isnull=False)
            if orders.count() != 0 and orders.count() == user.permission_level:
                return response.Response(
                    data={
                        "sucess": True,
                    }, 
                    status=status.HTTP_200_OK
                )
            else:
                order, created = Order.objects.get_or_create(user=user, able_to_raise_permission=True)
                if created:
                    token = order.create_device().token
                else:
                    token = None
                return response.Response(
                    data = {
                        "success": True, 
                        "token": token
                    },
                    status=status.HTTP_201_CREATED
                )
        else:
            return response.Response(
                data={
                    "sucess": False,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class ProductAPIView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]
    serializer_class = OrderModelSerializer

    def post(self, request):
        print(request.data)
        try:
            user_id = request.data.get("user")
            reg_token = request.data.get("Reg-token")
        except KeyError:
            message = "Something went Wrong"
            error = True
            product = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            print("KeyError in data gathering.")
        if user_id and user_id != "None":
            user = User.objects.get(pk=user_id)
            if reg_token:
                order = Order.objects.get(user=user)
                if str(order.device_token.token) == reg_token:
                    message = "Congrats you have access to product."
                    error = False
                    product = True
                    status_code = status.HTTP_200_OK
                else:
                    message = "You dont have access to product on this device."
                    error = False
                    product = False
                    status_code = status.HTTP_401_UNAUTHORIZED
            elif DeviceToken.objects.filter(user=user).exists():
                message = "You dont have access to product on this device."
                error = False
                product = False
                status_code = status.HTTP_200_OK
            else:
                message = "You havent bought any products yet."
                error = False
                product = False
                status_code = status.HTTP_200_OK
                
        else:
            message = "You have to login to access our products."
            error = False
            product = False
            status_code = status.HTTP_401_UNAUTHORIZED
        return response.Response(
            data= {"product": product, "error": error, "message": message}, 
            status=status_code
        )