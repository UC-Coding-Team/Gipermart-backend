import json

import requests
from django.conf import settings

PAYMART_URL = settings.PAYMART_URL
PAYMART_TOKEN = settings.PAYMART_TOKEN


def return_payload_for_paymart(payload: dict):
    products = payload.get("products")
    if products is not None:
        payload_for_paymart = dict()
        products_paymart = list()
        for product in products:
            product_paymart = dict()
            product_paymart["price"] = product.get("price")
            product_paymart["amount"] = product.get("amount")
            product_paymart["name"] = product.get("name")
            products_paymart.append(product_paymart)

        payload_for_paymart["limit"] = payload.get("limit")
        payload_for_paymart["payment_date"] = payload.get("payment_date")
        payload_for_paymart["buyer_phone"] = payload.get("buyer_phone")
        payload_for_paymart["products"] = products_paymart
        return payload_for_paymart
    return payload


def paymart_request(payload: dict, suffix_url):
    payload = return_payload_for_paymart(payload)
    try:
        url = f"{PAYMART_URL}{suffix_url}"
        headers = {
            "Authorization": f"Bearer {PAYMART_TOKEN}",
            "Content-Type": "application/json",
        }

        res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
        if res.status_code == 200:
            return res.json()
        else:
            try:
                res_body = res.json()
            except json.decoder.JSONDecodeError:
                res_body = res.text
            return {"error": "Paymart service does not respond success"}
    except ConnectionError:
        return {"error": "Connection problem with Paymart service"}


def paymart_request_file(payload: dict, suffix_url):
    try:
        url = f"{PAYMART_URL}{suffix_url}"
        headers = {
            "Authorization": f"Bearer {PAYMART_TOKEN}",
        }
        files = {
            "passport_selfie": payload.pop("passport_selfie").file.getvalue(),
            "passport_first_page": payload.pop(
                "passport_first_page"
            ).file.getvalue(),
            "passport_with_address": payload.pop(
                "passport_with_address"
            ).file.getvalue(),
        }
        res = requests.post(
            url, headers=headers, data=payload, files=files, timeout=20
        )
        if res.status_code == 200:
            return res.json()
        else:
            return {"error": "Paymart service does not respond success"}
    except ConnectionError:
        return {"error": "Connection problem with Paymart service"}
