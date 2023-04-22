from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from social_media.models import UserProfile, Relationship, Post
from social_media.serializers import (
    UserProfilePhotoImageSerializer,
    UserProfileCreateSerializer,
    UserProfileRetrieveSerializer,
    UserProfileUpdateSerializer,
    UserProfileListSerializer,
    RelationshipCreateSerializer,
    RelationShipRetrieveSerializer,
    RelationshipDestroySerializer,
    PostListSerializer,
    PostCreateSerializer,
    PostDetailSerializer,

)


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
        return UserProfileListSerializer


class UserProfileView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):

    # TODO: Split different Serializer to different functions

    def get_object(self):
        return self.request.user.profile

    def get_serializer_class(self):
        if self.action == "upload-image":
            return UserProfilePhotoImageSerializer
        if self.action == "create":
            return UserProfileCreateSerializer
        if self.action == "retrieve":
            return UserProfileRetrieveSerializer
        if self.action == "update":
            return UserProfileUpdateSerializer
        return UserProfileRetrieveSerializer

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

##############################################################################


class FollowUser(generics.CreateAPIView):
    serializer_class = RelationshipCreateSerializer

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class UnfollowUser(generics.DestroyAPIView):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipDestroySerializer
    lookup_field = 'following__id'


class FollowersList(generics.ListAPIView):
    serializer_class = RelationShipRetrieveSerializer

    def get_queryset(self):
        user = self.request.user
        return Relationship.objects.filter(following=user)


class FollowingList(generics.ListAPIView):
    serializer_class = RelationShipRetrieveSerializer

    def get_queryset(self):
        user = self.request.user
        return Relationship.objects.filter(follower=user)

##############################################################################


class PostListView(generics.ListCreateAPIView, GenericViewSet):
    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return PostCreateSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostListFollowingView(APIView):
    def get(self, request):
        user_followings = Relationship.objects.filter(follower=request.user)
        following_ids = [user_following.following_id for user_following in user_followings]
        posts = Post.objects.filter(author_id__in=following_ids)
        serializer = PostListSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class PostDetailView(generics.RetrieveUpdateDestroyAPIView, GenericViewSet):
    def get_object(self):
        return Post.objects.get(id=self.kwargs.get("pk"))

    def get_serializer_class(self):
        return PostDetailSerializer
