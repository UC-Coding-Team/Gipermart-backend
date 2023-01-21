from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView

from apps.user_profile.models import User
from apps.paymart.schema import from_global_id_or_error
from .serializers import (
    PhoneVerifySerializer,
    CheckSmsCodeSerializer,
    AddCardSerializer,
    CheckAddCardSerializer,
    AddPassportSerializer,
    AddGuarantSerializer,
    AddBuyerSerializer,
    ContractSerializer,
    CheckUserSmsSerializer,
    PartnerConfirmSerializer,
    CancelContractSerializer,
)
from .services import (
    verify,
    send_sms_code,
    check_sms_code,
    add_card,
    check_add_card,
    add_passport,
    add_guarant,
    add_buyer,
    add_credit,
    check_user_sms,
    partner_confirm,
    cancel_credit,
)


def get_status_code(res):
    # status must be code
    if res.get('status') == '400':
        status_code = status.HTTP_400_BAD_REQUEST
    elif res.get('status') == '404':
        status_code = status.HTTP_404_NOT_FOUND
    else:
        status_code = status.HTTP_200_OK
    return status_code


class PhoneVerifyView(CreateAPIView):
    serializer_class = PhoneVerifySerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = verify(serializer.validated_data)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "error" in response
            else status.HTTP_200_OK
        )
        return Response(response, status=status_code)


class SendSmsCodeView(CreateAPIView):
    serializer_class = PhoneVerifySerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = send_sms_code(serializer.validated_data)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "error" in response
            else status.HTTP_200_OK
        )
        return Response(response, status=status_code)


class CheckSmsCodeView(CreateAPIView):
    serializer_class = CheckSmsCodeSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = check_sms_code(serializer.validated_data)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "error" in response
            else status.HTTP_200_OK
        )
        return Response(response, status=status_code)


class AddBuyerView(CreateAPIView):
    serializer_class = AddBuyerSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = add_buyer(serializer.validated_data)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "error" in response
            else status.HTTP_200_OK
        )
        return Response(response, status=status_code)


class AddCardView(CreateAPIView):
    serializer_class = AddCardSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = add_card(serializer.validated_data)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "error" in response
            else status.HTTP_200_OK
        )
        return Response(response, status=status_code)


class CheckAddCardView(CreateAPIView):
    serializer_class = CheckAddCardSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = check_add_card(serializer.validated_data)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "error" in response
            else status.HTTP_200_OK
        )
        return Response(response, status=status_code)


class AddPassportView(CreateAPIView):
    serializer_class = AddPassportSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["step"] = 2
        response = add_passport(data)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "error" in response
            else status.HTTP_200_OK
        )
        return Response(response, status=status_code)


class AddGuarantView(CreateAPIView):
    serializer_class = AddGuarantSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        response = add_guarant(data)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "error" in response
            else status.HTTP_200_OK
        )
        return Response(response, status=status_code)


class AddContractView(CreateAPIView):
    serializer_class = ContractSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        _, request.data["user"] = from_global_id_or_error(request.data.get('user_id'), User)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        response = add_credit(data)
        if response.get('status') == 1:
            self.perform_create(serializer, response.get('paymart_client')['contract_id'])
        status_code = get_status_code(response)
        return Response(response, status=status_code)

    def perform_create(self, serializer, contract_id=None):
        serializer.save(contract_id=contract_id)


class CancelContractView(CreateAPIView):
    serializer_class = CancelContractSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = cancel_credit(serializer.validated_data)
        status_code = get_status_code(response)
        return Response(response, status=status_code)


class CheckUserSmsView(CreateAPIView):
    serializer_class = CheckUserSmsSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = check_user_sms(serializer.validated_data)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "error" in response
            else status.HTTP_200_OK
        )
        return Response(response, status=status_code)


class PartnerConfirmView(CreateAPIView):
    serializer_class = PartnerConfirmSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = partner_confirm(serializer.validated_data)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "error" in response
            else status.HTTP_200_OK
        )
        return Response(response, status=status_code)
