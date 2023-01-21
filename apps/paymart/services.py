from .utils import paymart_request, paymart_request_file


def verify(payload: dict):
    suffix_url = "buyers/verify"
    return paymart_request(payload, suffix_url)


def send_sms_code(payload: dict):
    suffix_url = "partner/buyers/send-sms-code"
    return paymart_request(payload, suffix_url)


def check_sms_code(payload: dict):
    suffix_url = "partner/buyers/check-sms-code"
    return paymart_request(payload, suffix_url)


def add_buyer(payload: dict):
    suffix_url = "partner/buyers/add"
    return paymart_request(payload, suffix_url)


def add_card(payload: dict):
    suffix_url = "buyer/send-sms-code-uz"
    buyer_add_payload = {"phone": payload["phone"], "step": 1}
    add_buyer(buyer_add_payload)
    return paymart_request(payload, suffix_url)


def check_add_card(payload: dict):
    suffix_url = "buyer/check-sms-code-uz"
    return paymart_request(payload, suffix_url)


def add_passport(payload: dict):
    suffix_url = "partner/buyers/modify"
    return paymart_request_file(payload, suffix_url)


def add_guarant(payload: dict):
    suffix_url = "buyer/add-guarant"
    return paymart_request(payload, suffix_url)


def add_credit(payload: dict):
    suffix_url = "buyers/credit/add"
    return paymart_request(payload, suffix_url)


def cancel_credit(payload: dict):
    suffix_url = "buyers/credit/cancel"
    return paymart_request(payload, suffix_url)


def check_user_sms(payload: dict):
    suffix_url = "buyers/check-user-sms"
    return paymart_request(payload, suffix_url)


def partner_confirm(payload: dict):
    suffix_url = "/buyers/partner-confirm"
    return paymart_request(payload, suffix_url)
