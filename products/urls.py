from django.urls import path
from . import views

urlpatterns = [
    path("api/product/create/", views.ProductReplicaCreateAPIView.as_view()),
]    

