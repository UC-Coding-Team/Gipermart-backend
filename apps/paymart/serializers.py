from phonenumber_field.phonenumber import to_python
from rest_framework import serializers, status
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.response import Response

from .models import Contract


class CustomPhoneNumberField(PhoneNumberField):
    def to_internal_value(self, data):
        phone_number = to_python(data)
        if phone_number and not phone_number.is_valid():
            return Response({"status": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)
        return phone_number.as_e164


class PhoneVerifySerializer(serializers.Serializer):
    phone = CustomPhoneNumberField(required=True)


class CheckSmsCodeSerializer(serializers.Serializer):
    phone = CustomPhoneNumberField(required=True)
    code = serializers.CharField(max_length=4)
    hashedCode = serializers.CharField(max_length=100)


class AddBuyerSerializer(serializers.Serializer):
    phone = CustomPhoneNumberField(required=True)
    step = serializers.IntegerField()


class AddCardSerializer(serializers.Serializer):
    phone = CustomPhoneNumberField(required=True)
    card = serializers.CharField(max_length=16)
    exp = serializers.CharField(max_length=5)


class CheckAddCardSerializer(serializers.Serializer):
    phone = CustomPhoneNumberField(required=True)
    card_number = serializers.CharField(max_length=16)
    card_valid_date = serializers.CharField(max_length=5)
    buyer_id = serializers.CharField()
    code = serializers.CharField()
    hashedCode = serializers.CharField()


class AddPassportSerializer(serializers.Serializer):
    passport_selfie = serializers.ImageField()
    passport_first_page = serializers.ImageField()
    passport_with_address = serializers.ImageField()
    buyer_id = serializers.CharField()


class AddGuarantSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = CustomPhoneNumberField()
    buyer_id = serializers.CharField()


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = (
            'user',
            'product_variant',
            'status',
            'products',
            'limit',
            'address',
            'payment_date',
            'buyer_phone',
            'created_at',
            'total_price',
            'total_count',
        )


class CancelContractSerializer(serializers.Serializer):
    contract_id = serializers.CharField()
    buyer_phone = serializers.CharField()


class CheckUserSmsSerializer(serializers.Serializer):
    phone = CustomPhoneNumberField(required=True)
    contract_id = serializers.CharField()
    code = serializers.CharField()


class PartnerConfirmSerializer(serializers.Serializer):
    contract_id = serializers.CharField()
