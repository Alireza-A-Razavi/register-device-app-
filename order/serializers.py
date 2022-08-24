from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db import IntegrityError
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import DeviceToken, PaidOrder, ProductLine
from account.utils import generate_random_password
from account.serializers import UserDetailSerializer
from products.models import Product
from products.serializers import ProductSerializer
from .utils import perform_raise_permission

User = get_user_model()

class InternalServerError(Exception):
    pass

class DeviceTokenModelSerializer(serializers.Serializer):
    token = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        user = self.context["request"].user
        device_token = user.create_device(product_id=self.context["request"].data.get("product_id"))
        return device_token


class VerifyDeviceTokenSerializer(serializers.Serializer):
    token = serializers.UUIDField(required=True)
    order_id = serializers.IntegerField(required=False)

    def validate_the_token(self, validated_data):
        order = PaidOrder.objects.get(wp_order_id=validated_data["order_id"])
        if order.device_token.token == validated_data["token"]:
            return True
        else:
            return False

class LineModelSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="item.pk")

    class Meta:
        model = ProductLine
        fields = ("product_id", "quantity",)

    def create(self, validated_data):
        product_wp_id = validated_data.pop("item")
        line, created = ProductLine.objects.get_or_create(
            item=Product.objects.get(wp_product_id=product_wp_id["pk"]),
            quantity=validated_data["quantity"],
        )
        from .utils import perform_raise_permission
        return line

class OrderModelSerializer(WritableNestedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())
    id = serializers.CharField(source="wp_order_id")
    status = serializers.CharField(required=False, write_only=True)
    customer_id = serializers.CharField(source="wp_user_id")
    line_items = LineModelSerializer(many=True)

    class Meta:
        model = PaidOrder
        fields = (
            "pk",
            "id",
            "created_at",
            "user",
            "status", 
            "customer_id",
            "line_items",
        )
        read_only_fields = ("user", "created_at")

    # take the user as there is no auth
    def create(self, validated_data):
        print(validated_data)
        _temp = validated_data
        if _temp.pop("status") == "completed":
            try:
                user = User.objects.get(
                    wp_user_id=_temp["wp_user_id"]
                )
            except User.DoesNotExist:
                raise ObjectDoesNotExist("User with this username doesn't exist")
            _temp["user"] = user
            try:
                create = super().create(_temp)
                perform_raise_permission(order=create, user=user)
                return create
            except IntegrityError:
                raise serializers.ValidationError("Order already exists")
        else:
            raise PermissionDenied


class DeviceAddPluginSerialzier(serializers.Serializer):
    plugin_id = serializers.IntegerField(write_only=True)
    token = serializers.UUIDField()

    def create(self, validated_data):
        user = self.context["request"].user
        product_perm = user.product_permissions.all().filter(product__wp_product_id=validated_data["plugin_id"]).first()
        if product_perm.check_device_limit():
            token = DeviceToken.objects.get(token=validated_data["token"])
            token.plugins.add(product_perm.product)
            token.save()
            product_perm.device_count += 1
            product_perm.save()
            return token
        else:
            raise serializers.ValidationError("You have reached this plugin device limit")


class DeviceInfoSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    plugins = ProductSerializer(many=True)

    class Meta:
        model = DeviceToken
        fields = (
            "created_at", 
            "user", 
            "plugins",
        )
