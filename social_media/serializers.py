from rest_framework import serializers

from social_media.models import UserProfile, Relationship, Post


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def validate(self, data):
        user = self.context["request"].user

        if hasattr(user, "profile") and user.profile:
            raise serializers.ValidationError("User already has a profile.")

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        profile = UserProfile.objects.create(**validated_data)
        user.profile = profile
        user.save()

        return profile


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only = "__all__"


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserProfilePhotoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "photo_image",
        )


class RelationShipRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = (
            "created_at",
            "following",
        )
        read_only = "__all__"


class RelationshipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ("id", "following", "created_at")


class RelationshipDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ("id", "following", "follower", "created_at")


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "content",
            "image",
            "hashtag",
        )

    def to_internal_value(self, data):
        data = data.copy()
        if "hashtag" in data:
            hashtag = data["hashtag"]
            if not hashtag.startswith("#"):
                hashtag = f"#{hashtag}"
            data["hashtag"] = hashtag
        return super().to_internal_value(data)


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "content",
            "author",
            "image",
            "hashtag",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "content",
            "image",
            "hashtag",
        )
