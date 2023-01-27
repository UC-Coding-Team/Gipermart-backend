from elasticsearch_dsl import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.products.serializers import ProductSerializer
from .documents import ProductDocument

class ProductSearch(APIView):
    serializer_class = ProductSerializer
    document_class = ProductDocument

    def generate_q_expression(self, query):
        return Q("match", name={"query":query, "fuzziness":"auto"})

    def get(self,request, query):
        q = self.generate_q_expression(query)
        search = self.document_class.search().query(q)
        return Response(self.serializer_class(search.to_queryset(), many=True).data)