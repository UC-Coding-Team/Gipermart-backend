from pprint import pprint

from apps.PaYme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="",
    paycom_id=""
)

resp = client._cards_create(
    number="",
    expire="",
    save=True,
)

pprint(resp)