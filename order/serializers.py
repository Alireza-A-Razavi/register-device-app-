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
            "user",
            "token",
            "created_at", 
            "refresh_time",
        )
        read_only_fields = ("created_at", "refresh_time",)
    
    def create(self, validated_data):
        order = PaidOrder.objects.get(pk=validated_data["order_id"])
        order.create_device
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


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
    username = serializers.CharField(read_only=True, source="user.username")
    user_password = serializers.CharField(read_only=True, source="user.temp_password")

    class Meta:
        model = PaidOrder
        fields = (
            "wp_user_id", 
            "wp_order_id",
            "created_at",
            "user",
            "username",
            "user_password",
        )
        read_only_fields = ("username", "user_passowrd", "user", "created_at")

    # take the user as there is no auth
    def create(self, validated_data):
        _temp = validated_data
        user = User.objects.get(
            wp_user_id=validated_data["wp_user_id"]
        )
        password = generate_random_password()
        user.temp_password = password
        user.set_password(password)
        user.save()
        print(validated_data)
        _temp["user"] = user
        return super().create(_temp)