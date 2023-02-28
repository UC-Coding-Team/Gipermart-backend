# send request to payme api

from pprint import pprint

from apps.PaYme.receipts.subscribe_receipts import PaymeSubscribeReceipts


rclient = PaymeSubscribeReceipts(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb",
    paycom_key="#MWnwHNYATJo%W@XvO5nISiY&mG7PEuzDX18"
)

resp = rclient._receipts_send(
    invoice_id="631186b6c4420cbf2712a243",
    phone="998901304527"
)

pprint(resp)