from django.urls import path

from . import views

urlpatterns = [
    path("phone-verify/", views.PhoneVerifyView.as_view(), name="phone_verify"),
    path("send-sms-code/", views.SendSmsCodeView.as_view(), name="send_sms_code"),
    path("check-sms-code/", views.CheckSmsCodeView.as_view(), name="check_sms_code"),
    path("add-buyer/", views.AddBuyerView.as_view(), name="add_buyer"),
    path("add-card/", views.AddCardView.as_view(), name="add_card"),
    path("check-add-card/", views.CheckAddCardView.as_view(), name="check_add_card"),
    path("add-passport/", views.AddPassportView.as_view(), name="add_passport"),
    path("add-guarant/", views.AddGuarantView.as_view(), name="add_guarant"),
    path("add-contract/", views.AddContractView.as_view(), name="add_contract"),
    path("cancel-contract/", views.CancelContractView.as_view(), name="cancel_contract"),
    path("check-user-sms/", views.CheckUserSmsView.as_view(), name="check_user_sms"),
    path("partner-confirm/", views.PartnerConfirmView.as_view(), name="partner_confirm"),
]
