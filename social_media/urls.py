from django.urls import path, include
from rest_framework import routers

from social_media.views import UserProfileView, UserProfilesListView

router = routers.DefaultRouter()
router.register("profiles", UserProfilesListView, basename="profiles")

urlpatterns = [
    path("", include(router.urls)),
    path("profile/create/", UserProfileView.as_view({"post": "create"})),
    path("profile/", UserProfileView.as_view({"get": "retrieve"})),
    path("profile/update/", UserProfileView.as_view({"put": "update"})),
]


app_name = "social_media"