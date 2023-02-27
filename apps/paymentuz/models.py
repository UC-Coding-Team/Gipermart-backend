from decimal import Decimal
from operator import attrgetter

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import JSONField  # type: ignore
from django.db.models.signals import post_save
from django.dispatch import receiver
from prices import Money

from ..checkout.models import Checkout
# from ..core.models import ModelWithMetadata
# from ..core.permissions import PaymentPermissions
# from ..core.taxes import zero_money
from . import ChargeStatus, CustomPaymentChoices, StorePaymentMethod, TransactionKind
# from ..account.validators import validate_possible_number
from phonenumber_field.modelfields import PhoneNumberField

# from ..order.services import send_telegram_notification

from django.core.exceptions import ValidationError
from phonenumber_field.phonenumber import to_python
from phonenumbers.phonenumberutil import is_possible_number

from .error_codes import AccountErrorCode


def validate_possible_number(phone, country=None):
    phone_number = to_python(phone, country)
    if (
        phone_number
        and not is_possible_number(phone_number)
        or not phone_number.is_valid()
    ):
        raise ValidationError(
            "The phone number entered is not valid.", code=AccountErrorCode.INVALID
        )
    return phone_number



def zero_money(currency: str) -> Money:
    """Return a money object set to zero.

    This is a function used as a model's default.
    """
    return Money(0, currency)



class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_number]


class Payment(models.Model):
    """A model that represents a single payment.

    This might be a transactable payment information such as credit card
    details, gift card information or a customer's authorization to charge
    their PayPal account.

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
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH
    )  # FIXME: add ISO4217 validator

    checkout = models.ForeignKey(
        Checkout, null=True, related_name="payments", on_delete=models.SET_NULL
    )
    # order = models.ForeignKey(
    #     Checkout, null=True, related_name="payments", on_delete=models.PROTECT
    # )
    store_payment_method = models.CharField(
        max_length=11,
        choices=StorePaymentMethod.CHOICES,
        default=StorePaymentMethod.NONE,
    )

    billing_phone = PossiblePhoneNumberField(blank=True)
    billing_first_name = models.CharField(max_length=256, blank=True)
    billing_last_name = models.CharField(max_length=256, blank=True)
    billing_company_name = models.CharField(max_length=256, blank=True)
    billing_address_1 = models.CharField(max_length=256, blank=True)
    billing_address_2 = models.CharField(max_length=256, blank=True)
    billing_city = models.CharField(max_length=256, blank=True)
    billing_city_area = models.CharField(max_length=128, blank=True)
    billing_postal_code = models.CharField(max_length=256, blank=True)
    billing_country_code = models.CharField(max_length=2, blank=True)
    billing_country_area = models.CharField(max_length=256, blank=True)

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

    class Meta:
        ordering = ("pk",)
        # permissions = (
        #     (
        #         PaymentPermissions.HANDLE_PAYMENTS.codename,
        #         "Handle payments",
        #     ),
        # )
        # indexes = [
        #     *ModelWithMetadata.Meta.indexes,
        #     # Orders filtering by status index
        #     GinIndex(fields=["order_id", "is_active", "charge_status"]),
        # ]

    def __repr__(self):
        return "Payment(gateway=%s, is_active=%s, created=%s, charge_status=%s)" % (
            self.gateway,
            self.is_active,
            self.created,
            self.charge_status,
        )

    def get_last_transaction(self):
        return max(self.transactions.all(), default=None, key=attrgetter("pk"))

    def get_total(self):
        return Money(self.total, self.currency)

    def get_authorized_amount(self):
        money = zero_money(self.currency)

        # Query all the transactions which should be prefetched
        # to optimize db queries
        transactions = self.transactions.all()

        # There is no authorized amount anymore when capture is succeeded
        # since capture can only be made once, even it is a partial capture
        if any(
                [
                    txn.kind == TransactionKind.CAPTURE and txn.is_success
                    for txn in transactions
                ]
        ):
            return money

        # Filter the succeeded auth transactions
        authorized_txns = [
            txn
            for txn in transactions
            if txn.kind == TransactionKind.AUTH
               and txn.is_success
               and not txn.action_required
        ]

        # Calculate authorized amount from all succeeded auth transactions
        for txn in authorized_txns:
            money += Money(txn.amount, self.currency)

        # If multiple partial capture is supported later though it's unlikely,
        # the authorized amount should exclude the already captured amount here
        return money

    def get_captured_amount(self):
        return Money(self.captured_amount, self.currency)

    def get_charge_amount(self):
        """Retrieve the maximum capture possible."""
        return self.total - self.captured_amount

    @property
    def is_authorized(self):
        return any(
            [
                txn.kind == TransactionKind.AUTH
                and txn.is_success
                and not txn.action_required
                for txn in self.transactions.all()
            ]
        )

    @property
    def not_charged(self):
        return self.charge_status == ChargeStatus.NOT_CHARGED

    def can_authorize(self):
        return self.is_active and self.not_charged

    def can_capture(self):
        if not (self.is_active and self.not_charged):
            return False
        return True

    def can_void(self):
        return self.not_charged and self.is_authorized

    def can_refund(self):
        can_refund_charge_status = (
            ChargeStatus.PARTIALLY_CHARGED,
            ChargeStatus.FULLY_CHARGED,
            ChargeStatus.PARTIALLY_REFUNDED,
        )
        return self.charge_status in can_refund_charge_status

    def can_confirm(self):
        return self.is_active and self.not_charged

    def is_manual(self):
        return self.gateway == CustomPaymentChoices.MANUAL

    @property
    def is_cash(self):
        if self.gateway == 'mirumee.payments.payme':
            return False
        return True


# @receiver(post_save, sender=Payment)
# def send_notification(sender, instance, created, **kwargs):
#     if created:
#         send_telegram_notification(instance, 'payment')


class Transaction(models.Model):
    """Represents a single payment operation.

    Transaction is an attempt to transfer money between your store
    and your customers, with a chosen payment method.
    """
    PROCESSING = 'processing'
    SUCCESS = 'success'
    FAILED = 'failed'
    CANCELED = 'canceled'
    STATUS = (
        (PROCESSING, 'processing'),
        (SUCCESS, 'success'),
        (FAILED, 'failed'),
        (CANCELED, 'canceled')
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)
    performed = models.DateTimeField(null=True)
    canceled = models.DateTimeField(null=True)
    payment = models.ForeignKey(
        Payment, related_name="transactions", on_delete=models.PROTECT
    )
    request_id = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    status = models.CharField(choices=STATUS, default='processing', max_length=55)
    token = models.CharField(max_length=512, blank=True, default="")
    kind = models.CharField(max_length=25, choices=TransactionKind.CHOICES)
    reason = models.IntegerField(null=True)
    is_success = models.BooleanField(default=False)
    action_required = models.BooleanField(default=False)
    action_required_data = JSONField(
        blank=True, default=dict, encoder=DjangoJSONEncoder
    )
    currency = models.CharField(max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH)
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
    already_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ("pk",)

    # def __repr__(self):
    #     return "Transaction(type=%s, is_success=%s, created=%s)" % (
    #         self.kind,
    #         self.is_success,
    #         self.created,
    #     )

    def get_amount(self):
        return Money(self.amount, self.currency)


class Currency(models.Model):
    currency = models.IntegerField()
