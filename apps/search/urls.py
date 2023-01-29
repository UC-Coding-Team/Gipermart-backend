from django.urls import path

from apps.search.views import SearchProductInventory

urlpatterns = [
    path("api/<str:query>/", SearchProductInventory.as_view()),
]
