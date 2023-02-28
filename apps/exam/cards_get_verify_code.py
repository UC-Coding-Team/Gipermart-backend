# send request to payme api

from pprint import pprint

from apps.PaYme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb"
)

resp = client._card_get_verify_code(
    token="63fd851c890565aa4e37bb93_25K3gGW2AokBtO9qYVpN0qz9WH3zUwtUH8vdepJURisqXgD9cEP64QqnJ0xoKDfp7hIF0KwisoDeOTGHzdAngq0Qqy8V3J7odIUrVtiUhnwb4xKZWUb5g9Vc5O5827hZ6dGRnuXuI5hCqSCqFOVqE1cmorxa1rrQNGVswpw9TD99mt62qgKNQoshXG9hCoX1e9o5uC0UEz5njV4ZpDTD3tqObB1xuJOMkHYmRORi1K4Vsa1TB05ECObcn96nnGUr00w1fMnkewzSwaxSUfrEHYBFYbCPoa0c2R8FgrbijsbMpGzVrorp74jD8gfh2I270sFR038thCgQNYOH1VynfN0t05Yr7H4sXeXYRnRnOg2IjXUuxZsCjAeGNJKG1hvwhpWKpt"
)

pprint(resp)