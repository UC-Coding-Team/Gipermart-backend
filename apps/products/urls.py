from django.urls import path

from . import views


urlpatterns = [
    path("category/", views.CategoryListAPIView.as_view()),
    path("category/<int:pk>/", views.CategoryAPIView.as_view()),
]