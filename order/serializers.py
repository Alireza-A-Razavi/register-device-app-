from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import DeviceToken, PaidOrder
from account.utils import generate_random_password

User = get_user_model()

class InternalServerError(Exception):
    pass

class DeviceTokenModelSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()

    class Meta:
        model = DeviceToken
        fields = (
            "order_id",
            "token",
            "created_at", 
            "refresh_time",
        )
        read_only_fields = ("created_at", "refresh_time",)
    
    def create(self, validated_data):
        order = PaidOrder.objects.get(wp_order_id=validated_data["order_id"])
        device = order.create_device()
        return device


class VerifyDeviceTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    order_id = serializers.IntegerField(required=False)

    def validate_token(self, validated_data):
        device_token = DeviceToken.objects.filter(user=self.context["request"].user)
        validated_data = self.validated_data
        try:
            if validated_data["order_id"] != "" or None:
                device_token.filter(order_id=validated_data["order_id"])
        except:
            pass
        if device_token.first().token != validated_data["token"]:
            return False
        else:
            return True

class OrderModelSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())

    class Meta:
        model = PaidOrder
        fields = (
            "wp_user_id", 
            "wp_order_id",
            "created_at",
            "user",
        )
        read_only_fields = ("user", "created_at")

    # take the user as there is no auth
    def create(self, validated_data):
        _temp = validated_data
        user = User.objects.get(
            wp_user_id=validated_data["wp_user_id"]
        )
        _temp["user"] = user
        return super().create(_temp)