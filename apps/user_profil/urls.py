from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import (
    UserProfileViewSet,
    LoginViewSet,
    UserProfileFeedViewSet
    )

router = DefaultRouter()
router.register('profile', UserProfileViewSet, basename="profile" )
router.register('login', LoginViewSet, basename="login" )
router.register('feed', UserProfileFeedViewSet)

urlpatterns = [
    path('', include(router.urls)),
]