from pyexpat import model
from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now as timezone_now
from rest_framework import serializers

from . import ProductType

User = get_user_model()

class DeviceToken(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_time = models.DateTimeField(default=timezone_now)
    token = models.UUIDField(default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.token)

    
    def refresh_token(self):
        self.refresh_time = timezone_now()
        self.save()
        return True
    
class PaidOrder(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    wp_user_id = models.PositiveBigIntegerField()
    wp_order_id = models.PositiveBigIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid4, editable=False)
    device_token = models.OneToOneField(DeviceToken, on_delete=models.SET_NULL, null=True, blank=True)
    device_limit = models.IntegerField(default=0)
    product = models.ForeignKey(
        "products.Product", 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username} - order"
    
    def save(self, *args, **kwargs):
        if self.device_limit != 0:
            pass 
        elif self.product_type == ProductType.ALL_IN_ONE:
            self.device_limit = 10
        elif self.product_type == ProductType.PREMIUM:
            self.device_limit = 1
        else:
            pass 
        super(PaidOrder, self).save(*args, **kwargs)
    
    def create_device(self):
        if self.device_limit <= DeviceToken.objects.filter(user=self.user).count():
            raise serializers.ValidationError("You already have a product registered")
        else:
            device = DeviceToken.objects.create(user=self.user)
            self.device_token = device
            self.save()
            return device