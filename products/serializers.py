from rest_framework import serializers

from .models import Product, PieceOfCode, ProductFile, ProductPermission

class ProductFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductFile
        fields = (
            "name",
            "associated_file",
        )

class ProductPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPermission
        fields = (
            "title", 
            "description",
            "device_count_permission",
        )

class PieceOfCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PieceOfCode
        fields = (
            "name",
            "code",
            "is_active",
        )

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="wp_product_id")
    permissions = ProductPermissionSerializer(many=True, read_only=True)
    files = ProductFileSerializer(many=True, read_only=True)
    codes = PieceOfCodeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "permalink",
            "id",
            "status",
            "permissions",
            "files",
            "codes",
        )