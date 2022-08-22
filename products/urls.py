from django.urls import path
from . import views

urlpatterns = [
    path("api/product/create/", views.ProductReplicaCreateAPIView.as_view()),

    path("api/proudct/<wp_product_id>/", views.ProductRetrieveAPIVIew.as_view()),

]    

