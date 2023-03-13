from django.conf import settings

from rest_framework import serializers

from .models import Order
from .models import MerchatTransactionsModel
from .errors.exceptions import IncorrectAmount
from .errors.exceptions import PerformTransactionDoesNotExist


class MerchatTransactionsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model: MerchatTransactionsModel = MerchatTransactionsModel
        fields: str = "__all__"

    def validate(self, data):
        """
        Validate the data given to the MerchatTransactionsModel.
        """
        if data.get("payment_id") is not None:
            try:
                order = Order.objects.get(
                    id=data['payment_id']
                )
                if order.amount != int(data['amount']):
                    raise IncorrectAmount()

            except IncorrectAmount:
                raise IncorrectAmount()

        return data

    def validate_amount(self, amount) -> int:
        """
        Validator for Transactions Amount
        """
        if amount is not None:
            if int(amount) <= settings.PAYME.get("PAYME_MIN_AMOUNT"):
                raise IncorrectAmount()

        return amount

    def validate_order_id(self, payment_id) -> int:
        """
        Use this method to check if a transaction is allowed to be executed.
        :param payment_id: string -> Order Indentation.
        """
        try:
            Order.objects.get(
                id=payment_id,
            )
        except Order.DoesNotExist:
            raise PerformTransactionDoesNotExist()

        return payment_id
