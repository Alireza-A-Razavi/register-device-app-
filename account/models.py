from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import PermissionDenied

from . import ProductPermissionType
from products import ProductType
from products.models import Product

class UserManager(BaseUserManager):
    def create_user(
        self, wp_user_id,wp_user_username,phone_number=None,email=None, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        if email:
            email = UserManager.normalize_email(email)

        user = self.model(
            phone_number=phone_number, email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, wp_user_id=-12, phone_number=None, email=None, password=None, **extra_fields):
        return self.create_user(
            wp_user_id ,password, phone_number, email=None, is_staff=True, is_superuser=True, **extra_fields
        )


    def staff(self):
        return self.get_queryset().filter(is_staff=True)


class User(AbstractUser):
    permission_level = models.PositiveIntegerField(default=0)
    wp_user_id = models.BigIntegerField(unique=True)
    wp_user_username = models.CharField(
        max_length=128,
        null=True, 
        blank=True,
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    products = models.ManyToManyField("products.Product", blank=True)

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()
    

    def check_permission_satisfied(self):
        pass

    # this piece of code, create_main_product_permission func, is for high scale
    # users for now I stick to perform_raise_permission in order/utils.py file to
    # achevie needs of quick delivery
    def create_main_product_permission(self, product_ids):
        if product_ids:
            # get products with passed list of ids
            products = Product.objects.filter(wp_product_id__in=prodcut_ids)
            # fetch products that already have permission associated with 
            # product ids and current user
            # -- first fetch perms  
            perms_already_there = UserProductPermission.objects.filter(
                product__in=products, user=self
            ).select_related("product")
            # then value of the ids of products have perm
            prods_have_perm = perms_already_there.values_list("product__id")
            # differetiate products that don't have permission associated
            target_prods = products.difference(prods_have_perm)
            # bulk create product permissions for target products
            users = UserProductPermission.objects.bulk_create(
                UserProductPermission(product=p, user=self) for p in target_prods
            )
            # update perms that are already there with device_count
            update_objs = []
            for perm in perms_already_there:
                perm.allowed_device_count += perm.product.device_count_limit
                update_objs.append(perm)
            UserProductPermission.objects.bulk_update(
                update_objs, ["allowed_device_count"]
            )
        else:
            return None

    def create_device(self, product_id):
        perm = self.product_permissions.filter(product__wp_product_id=product_id).first()
        if perm:
            if perm.check_device_limit():
                from order.models import DeviceToken
                device_token = DeviceToken.objects.create(user=self)
                perm.device_count += 1
                perm.save()
                return device_token
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
             

class UserProductPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_permissions")
    product = models.ForeignKey(
        "products.Product", 
        on_delete=models.CASCADE,
    )
    allowed_device_count = models.PositiveIntegerField(default=0)
    device_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        unique_together = ["product", "user"]

    def check_device_limit(self):
        if self.device_count != 0 and self.device_count > self.allowed_device_count:
            return False 
        elif self.device_count < self.allowed_device_count and self.allowed_device_count != 0:
            return True

    def up_device_count(self):
        self.device_count += 1
        self.save()
        return True

    def down_device_permission(self):
        self.device_count -+ 1
        self.save()
        return True

    def save(self, *args, **kwargs):
        if self.device_count != 0 and self.device_count > self.allowed_device_count:
            raise PermissionDenied
        else:
            super(UserProductPermission, self).save(*args, **kwargs)
