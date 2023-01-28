from django.urls import path
from .views import SearchProductInventory

urlpatterns = [
    path("api/<str:query>/", SearchProductInventory.as_view()),

]