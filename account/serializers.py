from rest_framework import serializers

from .models import User
from .utils import generate_random_password

class UserReplicaSerializer(serializers.Serializer):
    wp_user_id = serializers.IntegerField(required=False) # id showing the user id in wordpress db
    wp_user_username = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        try:
            validated_data["username"] = validated_data["phone_number"]
        except KeyError:
            validated_data["username"] = validated_data["wp_user_username"]
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"