from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from . import ProductPermissionType

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

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    def set_product_permission(self, permission=None):
        if not permission:
            return False
        elif permission == "premium":
            self.product_permission == ProductPermissionType.PREMIUM
            self.save()
            return self.product_permission
        elif permission == "all-in-one":
            self.product_permission = ProductPermissionType.ALL_IN_ONE
            self.save()
            return self.product_permission
        else:
            return False