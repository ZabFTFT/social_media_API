from django.urls import path, include
from rest_framework import routers

from social_media.views import UserProfileView, UserProfilesListView

router = routers.DefaultRouter()
router.register("profile", UserProfileView, basename="profile")
router.register("profiles", UserProfilesListView, basename="profiles")

urlpatterns = [
    path("", include(router.urls)),
    # path('follow/<int:pk>/', FollowView.as_view({'post': 'follow'})),
    # path('unfollow/<int:pk>/', FollowView.as_view({'post': 'unfollow'})),
]


app_name = "social_media"