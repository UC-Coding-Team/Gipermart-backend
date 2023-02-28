# send request to payme api

from pprint import pprint

from apps.PaYme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb",
    paycom_key="#MWnwHNYATJo%W@XvO5nISiY&mG7PEuzDX18"
)

resp = rclient._receipts_create(
    amount=10000,
    order_id="1"
)

pprint(resp)