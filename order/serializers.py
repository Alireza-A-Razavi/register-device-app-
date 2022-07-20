from rest_framework import serializers

from .models import DeviceToken, Order

class InternalServerError(Exception):
    pass

class DeviceTokenModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceToken
        fields = (
            "refresh_time",
            "user",
            "token",
        )

class OrderModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            "created_at",
            "token",
            "device_token",
            "able_to_raise_permission",
        )

    def create(self, validated_data, *args, **kwargs):
        token = DeviceTokenModelSerializer(data={"user": validated_data["user"]})
        if token.is_valid():
            token.save()
            super(OrderModelSerializer, self).save(validated_data, *args, **kwargs)
        else:
            print(token.errors)
            print("Device Token for order didn't created")
            raise InternalServerError