from itertools import product
from rest_framework import serializers

from .models import User, UserProductPermission
from .utils import generate_random_password

class UserReplicaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, source="wp_user_id") # id showing the user id in wordpress db
    wp_user_username = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"
        depth = 1

class UserProductPermissionSerializer(serializers.ModelSerializer):
    product_type = serializers.SerializerMethodField()

    class Meta:
        model = UserProductPermission
        fields = (
            "product_type",
            "allowed_device_count",
            "device_count",
        )
    
    def get_product_type(self, obj):
        return obj.product.product_type

class UserDetailSerializer(serializers.ModelSerializer):
    product_permissions = UserProductPermissionSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "products",
            "product_permissions",
        )