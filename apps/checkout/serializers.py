from rest_framework import serializers

from config import settings
from .models import Checkout
from apps.cart.serializers import CartItemSerializer
from ..PaYme.errors.exceptions import IncorrectAmount, PerformTransactionDoesNotExist


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ['id', 'full_name', 'phone_number', 'region', 'town', 'address', 'comment', 'cart', 'user', 'PAY_STATUS',
                  'NAXT_STATUS','total_price', 'created_at']

        def validate(self, data):
            """
            Validate the data given to the MerchatTransactionsModel.
            """
            if data.get("pk") is not None:
                try:
                    order = Checkout.objects.get(
                        id=data['pk']
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

        def validate_order_id(self, order_id) -> int:
            """
            Use this method to check if a transaction is allowed to be executed.
            :param order_id: string -> Order Indentation.
            """
            try:
                Checkout.objects.get(
                    id=id,
                )
            except Checkout.DoesNotExist:
                raise PerformTransactionDoesNotExist()

            return order_id


class CheckoutAllSerializer(serializers.ModelSerializer):
    cart = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Checkout
        fields = ['id','full_name', 'phone_number', 'region', 'town', 'address', 'comment', 'cart', 'PAY_STATUS',
                  'NAXT_STATUS', 'created_at','total_price','generate_link']
