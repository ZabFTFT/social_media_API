
from rest_framework import generics, mixins, status
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
    ModelViewSet
):

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
        userprofile = self.get_object()
        serializer = self.get_serializer(userprofile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUser(generics.CreateAPIView):
    serializer_class = RelationshipCreateSerializer

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class UnfollowUser(generics.DestroyAPIView):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipDestroySerializer
    lookup_field = "following__id"


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


class PostListView(
    generics.ListCreateAPIView
):
    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = Post.objects.all()
        hashtag = self.request.query_params.get("hashtag")
        content = self.request.query_params.get("content")
        authors = self.request.query_params.get("author")
        if hashtag:
            queryset = queryset.filter(hashtag__icontains=hashtag)
        if content:
            queryset = queryset.filter(content__icontains=content)
        if authors:
            authors_id = self._params_to_ints(authors)
            queryset = queryset.filter(author_id__in=authors_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCreateSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostListFollowingView(APIView):
    def get(self, request):
        user_followings = Relationship.objects.filter(follower=request.user)
        following_ids = [
            user_following.following_id for user_following in user_followings
        ]
        posts = Post.objects.filter(author_id__in=following_ids)
        serializer = PostListSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        return Post.objects.get(id=self.kwargs.get("pk"))

    def get_serializer_class(self):
        return PostDetailSerializer
