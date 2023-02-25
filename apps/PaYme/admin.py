
from django.contrib import admin

from .models import Order
from .models import MerchatTransactionsModel

admin.site.register(Order)
admin.site.register(MerchatTransactionsModel)