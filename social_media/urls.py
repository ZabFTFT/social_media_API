from django.urls import path, include
from rest_framework import routers

from social_media.views import UserProfileView, UserProfilesListView, \
    FollowUser, UnfollowUser, FollowersList, FollowingList, PostListView, PostDetailView, PostListFollowingView

router = routers.DefaultRouter()
router.register("profiles", UserProfilesListView, basename="profiles")

urlpatterns = [
    path("", include(router.urls)),
    path("profile/create/", UserProfileView.as_view({"post": "create"})),
    path("profile/", UserProfileView.as_view({"get": "retrieve"})),
    path("profile/update/", UserProfileView.as_view({"put": "update"})),
    path('follow/<int:id>/', FollowUser.as_view(), name='follow'),
    path('unfollow/<int:following__id>/', UnfollowUser.as_view(), name='unfollow'),
    path('followers/', FollowersList.as_view(), name='followers'),
    path('following/', FollowingList.as_view(), name='following'),
    path('posts/', PostListView.as_view({"post": "create"}), name='post-list'),
    path("posts/following/", PostListFollowingView.as_view(), name="post-list-following"),
    path('post/<int:pk>/', PostDetailView.as_view({
        "get": "retrieve",
         "put": "update",
         "patch": "partial_update",
         "delete": "destroy"
    }), name='post-detail'),
]


app_name = "social_media"