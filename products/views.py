from rest_framework import generics, authentication, permissions

from .models import Product
from .serializers import ProductSerializer

class ProductReplicaCreateAPIView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    