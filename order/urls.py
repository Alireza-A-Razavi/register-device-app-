from django.urls import path
from . import views

urlpatterns = [
    path("api/order/create/", views.ReplicaOrderCreateAPIView.as_view()),
    path("api/device/create/", views.DeviceTokenCreateAPIView.as_view()),
    path("api/device/verify/", views.DeviceTokenVerifyAPIView.as_view()),
]    

