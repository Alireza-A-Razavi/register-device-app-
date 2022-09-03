from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now as timezone_now

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
    product = models.ForeignKey("products.Product", blank=True, null=True, on_delete=models.SET_NULL)
    device_uuid = models.CharField(max_length=64, null=True, blank=True)
    expired = models.BooleanField(default=False, null=True, blank=True) # user expires it
   
    def __str__(self):
        return str(self.token)
    
    def refresh_token(self):
        self.refresh_time = timezone_now()
        self.token = uuid4()
        self.expired = False
        self.save()
        return self.token

    def activate_and_handle_plugins(self):
        # for sake of race condition and faster queies use bulk_update
        from account.models import UserProductPermission
        plugin_perms = UserProductPermission.objects.filter(user=self.user, product_type=ProductType.PLUGIN).select_related("product")
        for plugin_perm in plugin_perms:
            if not plugin_perm.check_device_limit():
                pass
            else:
                plugin_perm.up_device_count() 
                self.plugins.add(plugin_perm.product)
                self.save()


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
    rose_permission = models.BooleanField(default=False)
    line_items = models.ManyToManyField(ProductLine)

    def __str__(self):
        return f"{self.user.username} - order"

    def save(self, *args, **kwargs):
        print("save method is called:  ", self.id)
        super(PaidOrder, self).save(*args, **kwargs)
        if self.user and self.line_items:
            for p in self.line_items.all():
                self.user.products.add(p.item)