from django.urls import path
from .views import ProductSearch

urlpatterns = [
    path('search/<str:query>', ProductSearch.as_view()),
]