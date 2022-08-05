from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db import IntegrityError

from .models import DeviceToken, PaidOrder
from account.utils import generate_random_password

User = get_user_model()

class InternalServerError(Exception):
    pass

class DeviceTokenModelSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(write_only=False, source='paidorder.pk')
    token = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        try:
            order = PaidOrder.objects.get(wp_order_id=validated_data["paidorder"]["pk"])
        except PaidOrder.DoesNotExist:
            order = PaidOrder.objects.get(pk=validated_data["paidorder"]["pk"])
        device = order.create_device()
        return device


class VerifyDeviceTokenSerializer(serializers.Serializer):
    token = serializers.UUIDField(required=True)
    order_id = serializers.IntegerField(required=False)

    def validate_the_token(self, validated_data):
        order = PaidOrder.objects.get(wp_order_id=validated_data["order_id"])
        if order.device_token.token == validated_data["token"]:
            return True
        else:
            return False

class OrderModelSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())
    id = serializers.CharField(source="wp_order_id")
    status = serializers.CharField(required=False, write_only=True)
    customer_id = serializers.CharField(source="wp_user_id")

    class Meta:
        model = PaidOrder
        fields = (
            "pk",
            "id",
            "created_at",
            "user",
            "status", 
            "customer_id",
        )
        read_only_fields = ("user", "created_at")

    # take the user as there is no auth
    def create(self, validated_data):
        print(validated_data)
        _temp = validated_data
        if _temp.pop("status") == "paid":
            try:
                user = User.objects.get(
                    wp_user_id=_temp["wp_user_id"]
                )
            except User.DoesNotExist:
                raise ObjectDoesNotExist("User with this username doesn't exist")
            _temp["user"] = user
            try:
                return super().create(_temp)
            except IntegrityError:
                raise serializers.ValidationError("Order already exists")
        else:
            raise PermissionDenied