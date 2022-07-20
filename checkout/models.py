from decimal import Decimal
from statistics import mode
from uuid import uuid4

from django.conf import settings
from django.db import models


class Checkout(models.Model):
    """A shopping checkout."""

    created = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="checkouts",
        on_delete=models.CASCADE,
    )
    email = models.EmailField(blank=True, null=True)
    token = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    note = models.TextField(blank=True, default="")
    discount_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    total_amount = models.FloatField(default=0) #temp
    redirect_url = models.URLField(blank=True, null=True)
    tracking_code = models.CharField(max_length=255, blank=True, null=True)