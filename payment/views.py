from msilib.schema import Patch
from rest_framework import (
    views, 
    generics, 
    response, 
    status,
    authentication,
    permissions,
)

from .serializers import PaymentModelSerializer, TransactionModelSerializer

class CreatePaymentAPIView(generics.CreateAPIView):
    serializer_class = PaymentModelSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny] # for testing purpose
    # permission_classes = [permissions.IsAuthenticated]

class CreateTransactionAPIView(generics.CreateAPIView):
    serializer_class = TransactionModelSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny] # for testing purpose
    # permission_classes = [permissions.IsAuthenticated,]
