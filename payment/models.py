from decimal import Decimal

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.serializers.json import DjangoJSONEncoder

from . import ChargeStatus, TransactionKind

class Payment(models.Model):
    """A model that represents a single payment.

    This might be a transactable payment information such as credit card
    details, gift card information or a customer's authorization to charge
    their gateaway account.

    All payment process related pieces of information are stored
    at the gateway level, we are operating on the reusable token
    which is a unique identifier of the customer for given gateway.

    Several payment methods can be used within a single order. Each payment
    method may consist of multiple transactions.
    """

    gateway = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    to_confirm = models.BooleanField(default=False)
    partial = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    charge_status = models.CharField(
        max_length=20, choices=ChargeStatus.CHOICES, default=ChargeStatus.NOT_CHARGED
    )
    token = models.CharField(max_length=512, blank=True, default="")
    total = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    captured_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    checkout = models.ForeignKey(
        "checkout.Checkout", null=True, related_name="payments", on_delete=models.SET_NULL
    )
    order = models.ForeignKey(
        "order.Order", null=True, related_name="payments", on_delete=models.PROTECT
    )

    # billing_email = models.EmailField(blank=True)
    # billing_first_name = models.CharField(max_length=256, blank=True)
    # billing_last_name = models.CharField(max_length=256, blank=True)
    # billing_company_name = models.CharField(max_length=256, blank=True)
    # billing_address_1 = models.CharField(max_length=256, blank=True)
    # billing_address_2 = models.CharField(max_length=256, blank=True)
    # billing_city = models.CharField(max_length=256, blank=True)
    # billing_city_area = models.CharField(max_length=128, blank=True)
    # billing_postal_code = models.CharField(max_length=256, blank=True)
    # billing_country_code = models.CharField(max_length=2, blank=True)
    # billing_country_area = models.CharField(max_length=256, blank=True)

    cc_first_digits = models.CharField(max_length=6, blank=True, default="")
    cc_last_digits = models.CharField(max_length=4, blank=True, default="")
    cc_brand = models.CharField(max_length=40, blank=True, default="")
    cc_exp_month = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)], null=True, blank=True
    )
    cc_exp_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000)], null=True, blank=True
    )

    payment_method_type = models.CharField(max_length=256, blank=True)

    customer_ip_address = models.GenericIPAddressField(blank=True, null=True)
    extra_data = models.TextField(blank=True, default="")
    return_url = models.URLField(blank=True, null=True)
    psp_reference = models.CharField(
        max_length=512, null=True, blank=True, db_index=True
    )



class Transaction(models.Model):
    """Represents a single payment operation.

    Transaction is an attempt to transfer money between your store
    and your customers, with a chosen payment method.
    """

    created = models.DateTimeField(auto_now_add=True, editable=False)
    payment = models.ForeignKey(
        Payment, related_name="transactions", on_delete=models.PROTECT
    )
    token = models.CharField(max_length=512, blank=True, default="")
    kind = models.CharField(max_length=25, choices=TransactionKind.CHOICES)
    is_success = models.BooleanField(default=False)
    action_required = models.BooleanField(default=False)
    action_required_data = models.JSONField(
        blank=True, default=dict, encoder=DjangoJSONEncoder
    )
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    error = models.CharField(
        max_length=256,
        null=True,
    )
    customer_id = models.CharField(max_length=256, null=True)
    gateway_response = models.JSONField(encoder=DjangoJSONEncoder)
    already_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ("pk",)

    def __repr__(self):
        return "Transaction(type=%s, is_success=%s, created=%s)" % (
            self.kind,
            self.is_success,
            self.created,
        )