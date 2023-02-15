from django.http import HttpResponse
from apps.products.serializers import ProductInventorySearchSerializer
from apps.search.documents import ProductInventoryDocument
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView


class SearchProductInventory(APIView, LimitOffsetPagination):
    productinventory_serializer = ProductInventorySearchSerializer
    search_document = ProductInventoryDocument

    def get(self, request, query=None):
        try:
            q = Q(
                "bool",
                should=[
                    Q("match_phrase_prefix", product__name=query),
                    Q("match_phrase_prefix", product__description=query),
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
