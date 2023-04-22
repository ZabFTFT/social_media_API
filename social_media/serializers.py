from rest_framework import serializers

from social_media.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"


class UserProfileDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "mobile_number", "photo_image",)



class UserProfilePhotoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "photo_image",)