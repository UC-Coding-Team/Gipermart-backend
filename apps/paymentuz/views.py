from decimal import Decimal
# from saleor.graphql.payment.utils import convert_to_payme_amount
from . import ChargeStatus
from .lib.service import MerchantAPIView
from .lib.paycom import Paycom
from django.urls import path
from .models import Currency, Payment


def convert_to_payme_amount(amount):
    obj = Currency.objects.latest('id')
    if not obj:
        obj = Currency.objects.create(currency=11000)
    currency = obj.currency
    price = amount * currency
    return price*100


class CheckOrder(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        payment = Payment.objects.filter(pk=account['payment_id']).first()
        if payment:
            price = convert_to_payme_amount(payment.total)
            if float(amount) != float(price):
                return self.INVALID_AMOUNT
            if payment.charge_status == ChargeStatus.FULLY_CHARGED:
                return self.ORDER_NOT_FOND
            return self.ORDER_FOUND
        else:
            return self.ORDER_NOT_FOND

    def successfully_payment(self, account, transaction, *args, **kwargs):
        transaction.payment.charge_status = ChargeStatus.FULLY_CHARGED
        payment = transaction.payment
        payment.charge_status = ChargeStatus.FULLY_CHARGED
        payment.save()
        transaction.payment.captured_amount = transaction.payment.total
        transaction.payment.order.is_paid = True
        transaction.payment.order.captured_amount = transaction.payment.total
        transaction.payment.save()

    def cancel_payment(self, account, transaction, *args, **kwargs):
        transaction.payment.charge_status = ChargeStatus.CANCELLED
        transaction.payment.captured_amount = 0
        transaction.payment.save()
        transaction.payment.order.is_paid = False
        transaction.payment.order.captured_amount = 0
        transaction.payment.save()


class PaymentView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder


