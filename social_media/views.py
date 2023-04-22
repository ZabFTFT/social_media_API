from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from social_media.models import UserProfile
from social_media.serializers import UserProfileSerializer, UserProfilePhotoImageSerializer, UserProfileDetailSerializer


class UserProfilesListView(mixins.ListModelMixin, GenericViewSet):
    def get_queryset(self):
        queryset = UserProfile.objects.all()
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        email = self.request.query_params.get("email")

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(first_name__icontains=last_name)
        if email:
            queryset = queryset.filter(first_name__icontains=email)
        return queryset

    def get_serializer_class(self):
        return UserProfileSerializer


class UserProfileView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        queryset = UserProfile.objects.all()
        return queryset

    #TODO: Split different Serializer to different functions

    def get_serializer_class(self):
        if self.action == "upload-image":
            return UserProfilePhotoImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        userprofile = self.get_object()
        serializer = self.get_serializer(userprofile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class FollowView(viewsets.ViewSet):
#     queryset = UserProfile.objects.all()
#
#     def follow(self, request, pk):
#         own_profile = UserProfile.objects.get(user=self.request.user)
#         own_profile.following.add(
#             pk)
#         return Response({'message': 'now you are following'},
#                         status=status.HTTP_200_OK)
#
#     def unfollow(self, request, pk):
#         own_profile = UserProfile.objects.get(user=self.request.user)
#         own_profile.following.remove(pk)
#         return Response({'message': 'you are no longer following'}, status=status.HTTP_200_OK)
#
#
# class UserFollowersViewSet(
#     mixins.ListModelMixin,
#     viewsets.GenericViewSet,
# ):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileDetailSerializer
#
#     def get_queryset(self):
#         userprofile = UserProfile.objects.get(user=self.request.user)
#         print(type(userprofile))
#         return self.queryset.filter(following=userprofile)
