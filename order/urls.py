from django.urls import path
from . import views

urlpatterns = [
    path("api/order-create/", views.OrderCreateAPIView.as_view()),
    path("api/get-product/", views.ProductAPIView.as_view()),
    path("", views.IndexView.as_view()),
    path("order/", views.CreateOrderView.as_view()),
    path("product/", views.ProductPage.as_view()),
]
