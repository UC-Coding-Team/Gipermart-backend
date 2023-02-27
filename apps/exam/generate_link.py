# generate pay link (input)

from pprint import pprint

from apps.PaYme.methods.generate_link import GeneratePayLink

pay_link = GeneratePayLink(
  order_id=999,
  amount=9999
).generate_link()

pprint(pay_link)