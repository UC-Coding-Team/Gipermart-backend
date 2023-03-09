from django.http import HttpResponse
from apps.products.serializers import ProductInventorySearchSerializer
from apps.products.serializers import NewProductSerializer

from apps.search.documents import NewProductDocument
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView


class SearchProductInventory(APIView, LimitOffsetPagination):
    productinventory_serializer = ProductInventorySearchSerializer
    search_document = NewProductDocument

    def get(self, request, query=None):
        try:
            q = Q(
                "bool",
                should=[
                    Q("match_phrase_prefix", title=query),
                    Q("match_phrase_prefix", description=query),
                    Q("match_phrase_prefix", brand__name=query),
                ],
            )
            search = self.search_document.search().query(q)
            response = search.execute()

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.productinventory_serializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            return HttpResponse(e, status=500)
