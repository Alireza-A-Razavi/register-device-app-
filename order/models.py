from itertools import product
from pyexpat import model
from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now as timezone_now
from rest_framework import serializers

from products import ProductType


User = get_user_model()

class DeviceToken(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_time = models.DateTimeField(default=timezone_now)
    token = models.UUIDField(default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plugins = models.ManyToManyField(
        "products.Product", 
        blank=True,
        limit_choices_to={"product_type": ProductType.PLUGIN},
        related_name="linked_plugins",
    )
    expired = models.BooleanField(default=False, null=True, blank=True) # user expires it
   
    def __str__(self):
        return str(self.token)
    
    def refresh_token(self):
        self.refresh_time = timezone_now()
        self.token = uuid4()
        self.save()
        return True

    def activate_and_handle_plugins(self):
        from account.models import UserProductPermission
        plugin_perms = UserProductPermission.objects.filter(user=self.user)
        for plugin_perm in plugin_perms:
            if not plugin_perm.check_device_limit():
                pass
            else:
                plugin_perm.up_device_count() 


class ProductLine(models.Model):
    item = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"


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
    products = models.ManyToManyField("products.Product")
    rose_permission = models.BooleanField(default=False)
    line_items = models.ManyToManyField(ProductLine)

    def __str__(self):
        return f"{self.user.username} - order"
