from dataclasses import field, fields
from rest_framework import serializers

from .models import Payment, Transaction

class PaymentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "gateway",
            "total",
            "payment_method_type",
            "return_url",
            "customer_ip_address",
            
        )

class TransactionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            "payment",
            "kind", 
            "is_success",
            "gateway_response",
            "amount",
            "error",
            "token",
            "customer_id",
        )