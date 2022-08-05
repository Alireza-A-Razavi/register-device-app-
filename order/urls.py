from django.urls import path
from . import views

urlpatterns = [
    path("api/order/create/", views.ReplicaOrderCreateAPIView.as_view()),
    path("api/device/create/", views.DeviceTokenCreateAPIView.as_view()),
    path("api/device/verify/", views.DeviceTokenVerifyAPIView.as_view()),

    path("api/test/", views.TestOptionsAPIView.as_view()),

    path("register-product/", views.ValidateAndRegsiterUserView.as_view()),
    path("register-product/success/", views.SuccessProduct.as_view()),
]    

